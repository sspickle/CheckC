FROM debian:9.11

RUN apt-get update

RUN apt-get install -y gcc

RUN apt-get install -y valgrind

RUN apt-get install -y emacs-nox

RUN apt-get install -y clang-format

RUN apt-get install -y highlight

RUN apt-get install -y wget

RUN wget https://downloads.wkhtmltopdf.org/0.12/0.12.5/wkhtmltox_0.12.5-1.stretch_amd64.deb && \
    dpkg -i ./wkhtmltox_0.12.5-1.stretch_amd64.deb || true && \
    apt-get -f install -y && rm ./wkhtmltox_0.12.5-1.stretch_amd64.deb

COPY . /work

WORKDIR /work

CMD ["/bin/bash"]

