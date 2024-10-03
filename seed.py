import asyncio
from user.crud import retrieve_user_by_email, add_user


UserData = {
    "email": "superadmin@user.com",
    "password": "123123",
    "first_name": "super-admin",
    "last_name": "super-admin",
    "role": "admin"
}


async def create_admin_user():
    if await is_admin_user_present(): return

    await add_user(UserData)
    print("Admin user created successfully")

async def is_admin_user_present():
    if await retrieve_user_by_email("superadmin@user.com"):
        print("Admin user already exists. No new user created")
        return True
    return False

if __name__ == "__main__":
    asyncio.run(create_admin_user())
