FROM python:3.6.7-stretch AS base

ARG CHROME_DRIVER=2.43

ENV PYTHONUNBUFFERED 1

# Install chrome and chromedriver.
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list \
    && apt-get update -y && apt-get install -y google-chrome-stable unzip --no-install-recommends \
    && wget https://chromedriver.storage.googleapis.com/"${CHROME_DRIVER}"/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/bin/chromedriver \
    && chown root:root /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && apt-get purge --auto-remove -y unzip \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /src/*.deb

# Add chrome user.
RUN groupadd -r chrome && useradd -r -g chrome -G audio,video,voice chrome \
    && mkdir -p /home/chrome/Downloads /home/chrome/.config/google-chrome /data \
    && chown -R chrome:chrome /home/chrome && chown -R chrome:chrome /data

ADD main.py requirements.txt /opt/app/
WORKDIR /opt/app

RUN pip install -r requirements.txt \
    && pip install ipython

USER chrome

CMD ["/bin/bash"]
