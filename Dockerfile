#FROM gcc:8.3
FROM debian:9.11

RUN apt-get update

RUN apt-get install -y gcc

RUN apt-get install -y valgrind

RUN apt-get install -y emacs-nox

RUN apt-get install -y clang-format

RUN apt-get install -y highlight

RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN tar xvJf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz 
RUN cp wkhtmltox/bin/wkhtmlto* /usr/bin/

COPY . /work

WORKDIR /work

CMD ["/bin/bash"]

