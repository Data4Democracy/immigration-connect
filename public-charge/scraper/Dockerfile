FROM python:3.6.7-stretch AS base

ARG USER=chrome
ARG UID=1001
ARG CHROME_DRIVER=2.43

ENV PYTHONUNBUFFERED 1

# Install chrome, chromedriver, and xvfb.
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list \
    && apt-get update -y && apt-get install -y google-chrome-stable unzip xvfb --no-install-recommends \
    && wget https://chromedriver.storage.googleapis.com/"${CHROME_DRIVER}"/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/bin/chromedriver \
    && chown root:root /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && apt-get purge --auto-remove -y unzip \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /src/*.deb

# Add $USER user.
RUN groupadd -r "${USER}" \
    && useradd -r -g "${USER}" -u "${UID}" -G audio,video,voice "${USER}" \
    && mkdir -p /home/"${USER}"/Downloads /home/"${USER}"/.config/google-chrome /data \
    && chown -R "${USER}":"${USER}" /home/"${USER}" && chown -R "${USER}":"${USER}" /data

ADD scraper.py requirements.txt /opt/app/
WORKDIR /opt/app

RUN pip install -r requirements.txt \
    && pip install ipython

USER "${USER}"

CMD ["/bin/bash"]
