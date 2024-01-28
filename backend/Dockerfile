FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN git clone https://github.com/CASIA-IVA-Lab/FastSAM.git /tmp/FastSAM

RUN wget https://huggingface.co/spaces/An-619/FastSAM/resolve/main/weights/FastSAM.pt -P /code/models/FastSAM.pt

RUN pip install --no-cache-dir --upgrade -r /tmp/FastSAM/requirements.txt

RUN pip install --no-cache-dir git+https://github.com/openai/CLIP.git

RUN cd /tmp/FastSAM && pip install .

RUN rm -rf /tmp/FastSAM

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]