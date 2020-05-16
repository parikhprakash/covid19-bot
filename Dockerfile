FROM rasa/rasa-sdk:1.10.0

COPY actions.py /app/actions.py
COPY requirements-actions.txt /app/requirements-actions.txt

USER root
RUN pip install --no-cache-dir -r /app/requirements-actions.txt

USER 1001
CMD ["start", "--actions", "actions", "--debug"]