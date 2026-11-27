QUERY_SUMMARY = """
SELECT
    COUNT(*) AS total_users,
    COUNT(*) FILTER (WHERE messages_json::text != '[]') AS active_chats,
    COUNT(*) FILTER (WHERE is_paid = TRUE) AS paid_users
FROM users;
"""

QUERY_BRANCHES = """
SELECT 
    COALESCE(selected_category, 'не выбрана') AS category,
    COUNT(*) AS users_total,
    COUNT(*) FILTER (WHERE jsonb_array_length(messages_json) > 0) AS started_chat,
    COUNT(*) FILTER (WHERE is_paid = TRUE) AS paid
FROM users
GROUP BY selected_category
ORDER BY started_chat DESC;
"""

QUERY_FUNNEL = """
SELECT
    action,
    COUNT(*) AS total_count,
    COUNT(*) FILTER (WHERE created_at >= EXTRACT(EPOCH FROM CURRENT_DATE)) AS today_count
FROM audit_logs
GROUP BY action
ORDER BY today_count DESC, total_count DESC;
"""

QUERY_BLIND_SPOTS = """
SELECT 
    user_id,
    selected_category AS category,
    jsonb_array_length(messages_json) / 2 AS turns,
    to_timestamp(updated_at) AT TIME ZONE 'Europe/Moscow' AS last_msk,
    LEFT(messages_json->0->>'content', 90) AS first_question
FROM users
WHERE is_paid = FALSE AND jsonb_array_length(messages_json) >= 8
ORDER BY updated_at DESC LIMIT 20;
"""

QUERY_RECENT_USERS = """
SELECT 
    user_id,
    to_timestamp(updated_at) AT TIME ZONE 'Europe/Moscow' AS last_msk,
    selected_category AS category,
    is_paid,
    jsonb_array_length(messages_json) AS msgs,
    LEFT(messages_json->0->>'content', 80) AS first_question
FROM users
WHERE jsonb_array_length(messages_json) > 0
ORDER BY updated_at DESC LIMIT 15;
"""

QUERY_AUDIT_152FZ = """
SELECT jsonb_object_keys(mapping) AS created_tags
FROM (
    SELECT anonymizer_state_json->'mapping' AS mapping
    FROM users
    WHERE messages_json::text ILIKE '%РАСПОЗНАНО ЛОКАЛЬНО%'
    ORDER BY updated_at DESC LIMIT 1
) sub;
"""


def build_user_questions_query(user_id: str) -> str:
    return f"""
    SELECT m.ordinality AS num, m.msg->>'content' AS user_question
    FROM users u, LATERAL jsonb_array_elements(u.messages_json) WITH ORDINALITY AS m(msg, ordinality)
    WHERE u.user_id = {user_id} AND m.msg->>'role' = 'user'
    ORDER BY m.ordinality;
    """


def build_full_dialog_query(user_id: str) -> str:
    return f"""
    SELECT m.ordinality AS step, UPPER(m.msg->>'role') AS sender, m.msg->>'content' AS text
    FROM users u, LATERAL jsonb_array_elements(u.messages_json) WITH ORDINALITY AS m(msg, ordinality)
    WHERE u.user_id = {user_id}
    ORDER BY m.ordinality;
    """
