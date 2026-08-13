# Slim base image -- smaller download, smaller attack surface, faster
# deploys than the full python:3.12 image which includes a lot we don't need.
FROM python:3.12-slim

WORKDIR /app

# Copy requirements FIRST, before the rest of the code. This is a
# deliberate ordering, not an accident: Docker caches each instruction
# as a "layer." If requirements.txt hasn't changed, Docker reuses the
# cached "pip install" layer instead of re-running it -- so code changes
# (which happen constantly) don't force a slow dependency reinstall
# every single build. Copying everything at once would invalidate this
# cache on every code change, even a one-line fix.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the actual application code
COPY . .

# The trained classifier (.pkl) is deliberately gitignored -- trained
# artifacts don't belong in source control, only the code that produces
# them. But that means it doesn't exist yet inside a fresh image build
# either. Fix: generate the training data and train the model AS PART
# OF the build, so the image is self-contained and reproducible -- no
# manual "remember to copy the model in" step for whoever deploys this.
RUN cd ml && python generate_training_data.py && python train_classifier.py

EXPOSE 8000

# --host 0.0.0.0 is required, not optional, inside a container --
# uvicorn's default (127.0.0.1) only accepts connections from inside
# the container itself, which would make the API completely
# unreachable from outside, even with the port exposed above.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
