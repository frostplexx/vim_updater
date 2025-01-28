FROM python:3.9-slim

WORKDIR /app

COPY server.py .
COPY update_vimrc.sh .

LABEL "traefik.enable"="true"
LABEL "traefik.http.routers.vim_updater.rule"="Host(`vim.kuipr.de`)"
LABEL "traefik.http.routers.vim_updater.entrypoints"="websecure"
LABEL "traefik.http.routers.vim_updater.tls.certresolver"="myresolver"
LABEL "traefik.http.services.vim_updater.loadbalancer.server.port"="8080"

EXPOSE 8080

CMD ["python", "server.py"]
