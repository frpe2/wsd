from database.models import Cartridge, Status, CartridgeLog
from database.db import async_session
from sqlalchemy import select

async def log_action(cartridge_id, action, user):
    async with async_session() as session:
        log = CartridgeLog(
            cartridge_id=cartridge_id,
            action=action,
            user=user
        )
        session.add(log)
        await session.commit()


async def add_cartridge(model, owner, user):
    async with async_session() as session:
        c = Cartridge(model=model, owner=owner)
        session.add(c)
        await session.commit()
        await log_action(c.id, "Создан", user)


async def get_all():
    async with async_session() as session:
        result = await session.execute(select(Cartridge))
        return result.scalars().all()


async def get_by_status(status):
    async with async_session() as session:
        result = await session.execute(
            select(Cartridge).where(Cartridge.status == status)
        )
        return result.scalars().all()


async def search_cartridges(query):
    async with async_session() as session:
        result = await session.execute(
            select(Cartridge).where(
                Cartridge.model.ilike(f"%{query}%") |
                Cartridge.owner.ilike(f"%{query}%")
            )
        )
        return result.scalars().all()


async def update_status(cartridge_id, status, user):
    async with async_session() as session:
        c = await session.get(Cartridge, cartridge_id)
        c.status = status
        await session.commit()
        await log_action(cartridge_id, f"Статус → {status.value}", user)


async def update_cartridge(cartridge_id, model, owner, user):
    async with async_session() as session:
        c = await session.get(Cartridge, cartridge_id)
        c.model = model
        c.owner = owner
        await session.commit()
        await log_action(cartridge_id, "Отредактирован", user)


async def delete_cartridge(cartridge_id, user):
    async with async_session() as session:
        c = await session.get(Cartridge, cartridge_id)
        await session.delete(c)
        await session.commit()
        await log_action(cartridge_id, "Удален", user)


async def get_logs(cartridge_id):
    async with async_session() as session:
        result = await session.execute(
            select(CartridgeLog).where(CartridgeLog.cartridge_id == cartridge_id)
        )
        return result.scalars().all()