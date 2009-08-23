DROP DATABASE chula_session;

CREATE DATABASE chula_session WITH
    OWNER = postgres
    TEMPLATE = template0
    ENCODING = 'UTF-8';

CREATE USER chula;
ALTER USER chula WITH PASSWORD 'chula';

\c chula_session

-- Install LANGUAGE plpgsql;
CREATE FUNCTION plpgsql_call_handler() RETURNS language_handler AS
    '$libdir/plpgsql' LANGUAGE C;
CREATE FUNCTION plpgsql_validator(oid) RETURNS void AS
    '$libdir/plpgsql' LANGUAGE C;
CREATE TRUSTED PROCEDURAL LANGUAGE plpgsql
    HANDLER plpgsql_call_handler
    VALIDATOR plpgsql_validator;

-- Create the session table
CREATE TABLE session
(
    id SERIAL PRIMARY KEY,
    guid VARCHAR(64) UNIQUE NOT NULL,
    created TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMPTZ,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    values TEXT
);
GRANT ALL ON TABLE session TO chula;
GRANT ALL ON TABLE session_id_seq TO chula;

--Create an index on the guid
CREATE INDEX session_guid_idx ON session (guid);


-- Create the function used to persist session
-- Usage: SELECT session_set('abcdguid', '[1,2,3]', FALSE)
CREATE OR REPLACE FUNCTION session_set
(
    _guid VARCHAR(64),
    _values TEXT,
    _active BOOLEAN
)

RETURNS INT4 AS $session_set$
DECLARE
    result BOOLEAN;
    rs RECORD;

BEGIN
    IF LENGTH(_guid) != 64 THEN
        RAISE EXCEPTION 'The guid "%" was not a char(64)', _guid;
        RETURN -1;
    ELSE
        SELECT id, guid INTO rs FROM session
        WHERE guid = _guid;
        
        IF FOUND THEN
            --Update the existing session
            UPDATE session SET
                updated = CURRENT_TIMESTAMP,
                values = _values,
                active = _active
            WHERE guid = rs.guid;
                
            RETURN rs.id;
        ELSE
            --Create a new session
            INSERT INTO session(guid, values, active)
            VALUES(_guid, _values, TRUE);
            
            RETURN CURRVAL('session_id_seq');
        END IF;
    END IF;
END;
$session_set$ LANGUAGE plpgsql;

--EOF
