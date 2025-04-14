# alert.py (em /home/murilo/Documentos/Projetos/streamlit/lib/streamlit/elements/alert.py)

import logging
from typing import Optional

import streamlit as st
from streamlit.proto.Alert_pb2 import Alert

logging.basicConfig(
    filename="/home/murilo/Documentos/Projetos/streamlit/alert_debug.log",
    level=logging.DEBUG,
    format="%(levelname)s:%(name)s:%(message)s",
)

logging.debug("Carregando alert.py personalizado no log")
logging.debug("Definindo a classe AlertMixin personalizada")

class AlertMixin:
    def warning(self, body: str, *, icon: Optional[str] = None):
        logging.debug(f"Entrando na função warning do AlertMixin personalizado")
        logging.debug(f"warning - Initial body_str: {body!r}, icon: {icon!r}")

        starts_with_warning = body.startswith(":warning:")
        logging.debug(f"warning - Starts with :warning:? {starts_with_warning}")

        if starts_with_warning and icon is None:
            logging.debug("warning - Processing :warning: shortcode")
            body = body[len(":warning:") :].strip()
            icon = "⚠️"
        elif starts_with_warning and icon is not None:
            logging.debug("warning - Not processing shortcode")
            body = body.replace(":warning:", "[warning]")
        else:
            logging.debug("warning - Not processing shortcode")

        body = body.strip()
        logging.debug(f"warning - After clean_text: {body!r}, Final icon: {icon!r}")

        # Criar um AlertProto para o alerta
        alert_proto = Alert()
        alert_proto.body = body
        if icon is not None:
            alert_proto.icon = icon
        alert_proto.format = Alert.WARNING  # Equivalente a alert_type=1

        return self.dg._enqueue("alert", alert_proto)

    def info(self, body: str, *, icon: Optional[str] = None):
        logging.debug(f"Entrando na função info do AlertMixin personalizado")
        logging.debug(f"info - Initial body_str: {body!r}, icon: {icon!r}")

        starts_with_info = body.startswith(":info:")
        logging.debug(f"info - Starts with :info:? {starts_with_info}")

        if starts_with_info and icon is None:
            logging.debug("info - Processing :info: shortcode")
            body = body[len(":info:") :].strip()
            icon = "ℹ️"
        elif starts_with_info and icon is not None:
            logging.debug("info - Not processing shortcode")
            body = body.replace(":info:", "[info]")
        else:
            logging.debug("info - Not processing shortcode")

        body = body.strip()
        logging.debug(f"info - After clean_text: {body!r}, Final icon: {icon!r}")

        # Criar um AlertProto para o alerta
        alert_proto = Alert()
        alert_proto.body = body
        if icon is not None:
            alert_proto.icon = icon
        alert_proto.format = Alert.INFO  # Equivalente a alert_type=2

        return self.dg._enqueue("alert", alert_proto)

    def success(self, body: str, *, icon: Optional[str] = None):
        logging.debug(f"Entrando na função success do AlertMixin personalizado")
        logging.debug(f"success - Initial body_str: {body!r}, icon: {icon!r}")

        starts_with_success = body.startswith(":success:")
        logging.debug(f"success - Starts with :success:? {starts_with_success}")

        if starts_with_success and icon is None:
            logging.debug("success - Processing :success: shortcode")
            body = body[len(":success:") :].strip()
            icon = "✅"
        elif starts_with_success and icon is not None:
            logging.debug("success - Not processing shortcode")
            body = body.replace(":success:", "[success]")
        else:
            logging.debug("success - Not processing shortcode")

        body = body.strip()
        logging.debug(f"success - After clean_text: {body!r}, Final icon: {icon!r}")

        # Criar um AlertProto para o alerta
        alert_proto = Alert()
        alert_proto.body = body
        if icon is not None:
            alert_proto.icon = icon
        alert_proto.format = Alert.SUCCESS  # Equivalente a alert_type=3

        return self.dg._enqueue("alert", alert_proto)

    def error(self, body: str, *, icon: Optional[str] = None):
        body = body.strip()
        logging.debug(f"Entrando na função error do AlertMixin personalizado")
        logging.debug(f"error - After clean_text: {body!r}, Final icon: {icon!r}")

        # Criar um AlertProto para o alerta
        alert_proto = Alert()
        alert_proto.body = body
        if icon is not None:
            alert_proto.icon = icon
        alert_proto.format = Alert.ERROR  # Equivalente a alert_type=0

        return self.dg._enqueue("alert", alert_proto)

    @property
    def dg(self):
        return self