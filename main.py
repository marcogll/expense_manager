from loguru import logger
from talia.bot import create_bot
from db.init_db import Base, engine
from scheduler.jobs import setup_scheduler


def main():
    logger.info("Iniciando Talia & C.A.R.O.L.")

    # Inicializar base de datos
    from db.models import Base
    Base.metadata.create_all(bind=engine)
    logger.info("Base de datos inicializada")

    # Crear bot
    app = create_bot()

    # Iniciar scheduler
    setup_scheduler(app)

    logger.info("Bot iniciado. Esperando mensajes...")
    app.run_polling()


if __name__ == "__main__":
    main()
