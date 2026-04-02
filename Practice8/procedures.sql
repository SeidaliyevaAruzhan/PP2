-- INSERT OR UPDATE
CREATE OR REPLACE PROCEDURE insert_or_update_user_proc(
    p_name VARCHAR,
    p_surname VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM phonebook_proc
        WHERE name = p_name AND surname = p_surname
    ) THEN
        UPDATE phonebook_proc
        SET phone = p_phone
        WHERE name = p_name AND surname = p_surname;
    ELSE
        INSERT INTO phonebook_proc(name, surname, phone)
        VALUES (p_name, p_surname, p_phone);
    END IF;
END;
$$;


-- LOOP INSERT
CREATE OR REPLACE PROCEDURE insert_many_users_proc(
    p_names TEXT[],
    p_surnames TEXT[],
    p_phones TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(p_names, 1) LOOP
        IF length(p_phones[i]) < 10 THEN
            RAISE NOTICE 'Invalid phone: %', p_phones[i];
        ELSE
            INSERT INTO phonebook_proc(name, surname, phone)
            VALUES (p_names[i], p_surnames[i], p_phones[i]);
        END IF;
    END LOOP;
END;
$$;


-- DELETE
CREATE OR REPLACE PROCEDURE delete_user_proc(
    p_value VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook_proc
    WHERE name = p_value
       OR surname = p_value
       OR phone = p_value;
END;
$$;