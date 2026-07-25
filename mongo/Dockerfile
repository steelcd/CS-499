FROM mongo:8.3.4

COPY ./src/aac_shelter_outcomes.csv /tmp/data.csv
COPY ./src/rescue_profiles.json /tmp/rescue_profiles.json
COPY ./src/script.sh /docker-entrypoint-initdb.d/

RUN chmod +x /docker-entrypoint-initdb.d/script.sh
