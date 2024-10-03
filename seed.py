import asyncio
from user.crud import retrieve_user_by_email, add_user


async def create_admin_user():
    user_data = {
        "email": "superadmin@user.com",
        "password": "123123",
        "first_name": "super-admin",
        "last_name": "super-admin",
        "role": "admin"
    }

    if await is_admin_user_present():
        return

    await add_user(user_data)
    print("Admin user created successfully")

async def is_admin_user_present():
    existing_user = await retrieve_user_by_email("superadmin@user.com")
    if existing_user:
        print("Admin user already exists. No new user created")
        return True
    return False

if __name__ == "__main__":
    asyncio.run(create_admin_user())
