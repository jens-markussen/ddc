FROM python:3.14-slim

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

RUN apt-get update && apt-get install -y socat

WORKDIR /home/ctf

COPY ./flag.txt .
COPY ./chall.py .
RUN chmod 555 chall.py

RUN chown -R root:root /home/ctf
RUN chmod +xr /home/ctf

USER ctf

CMD socat -T60 TCP-LISTEN:1337,fork,reuseaddr EXEC:"python3 chall.py",stderr