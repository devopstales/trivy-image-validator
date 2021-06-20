FROM --platform=${TARGETPLATFORM:-linux/amd64} alpine:3.12 as base

RUN apk --no-cache add python3=3.8.10-r0 py3-pip=20.1.1-r0

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

RUN apk add --no-cache git && \
    addgroup -S -g 10001 kube-trivy-admission && \
    adduser -S -u 10001 kube-trivy-admission -G kube-trivy-admission && \
    mkdir /var/run/shell-operator && \
    chown -R kube-trivy-admission:kube-trivy-admission /var/run/shell-operator

COPY trivy /usr/local/bin
COPY server.pem /app
COPY trivy-scanner.py /app

USER 10001:10001

FROM base as prod
ENTRYPOINT [ "python3" ]
CMD [ "trivy-scanner.py" ]