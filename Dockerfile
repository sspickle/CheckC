FROM debian:9.11

RUN apt-get update

RUN apt-get install -y gcc

RUN apt-get install -y valgrind

RUN apt-get install -y emacs-nox

RUN apt-get install -y clang-format

RUN apt-get install -y highlight

RUN apt-get install -y wget

RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.stretch_amd64.deb && \
    dpkg -i ./wkhtmltox_0.12.6-1.stretch_amd64.deb || true && \
    apt-get -f install -y && rm ./wkhtmltox_0.12.6-1.stretch_amd64.deb

RUN apt-get install -y pandoc

RUN apt-get install -y ttf-ancient-fonts

COPY . /work

WORKDIR /work

CMD ["/bin/bash"]

