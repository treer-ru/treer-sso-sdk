from treer_sso_sdk import get_user_info_by_code
import asyncio

if __name__ == "__main__":
    user_info = asyncio.run(get_user_info_by_code(
        authorization_code="xQWJLoir8iXTQ4cy9LWLnLHXPqoqkKZB",
        client_id="123456789",
        client_secret="123456789",
        redirect_uri="https://qrfood.treer.ru",
    ))
    print(user_info.id, user_info.username, user_info.email, user_info.phone)
