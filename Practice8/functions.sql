-- SEARCH FUNCTION
CREATE OR REPLACE FUNCTION search_phonebook_proc(pattern_text TEXT)
RETURNS TABLE (
    id INT,
    name VARCHAR,
    surname VARCHAR,
    phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM phonebook_proc
    WHERE name ILIKE '%' || pattern_text || '%'
       OR surname ILIKE '%' || pattern_text || '%'
       OR phone ILIKE '%' || pattern_text || '%';
END;
$$;


-- PAGINATION FUNCTION
CREATE OR REPLACE FUNCTION get_phonebook_paginated(
    p_limit INT,
    p_offset INT
)
RETURNS TABLE (
    id INT,
    name VARCHAR,
    surname VARCHAR,
    phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM phonebook_proc
    LIMIT p_limit OFFSET p_offset;
END;
$$;