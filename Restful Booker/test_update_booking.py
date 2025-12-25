from constants import BASE_URL

class TestUpdateBooking:
    def test_update_booking(self, auth_session, booking_data, updated_booking_data):
        """
        Тест полного обновления бронирования
        """
        # Создание
        create_resp = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_resp.status_code == 200
        booking_id = create_resp.json()["bookingid"]

        # Обновление (PUT)
        update_resp = auth_session.put(
            f"{BASE_URL}/booking/{booking_id}",
            json=updated_booking_data
        )

        assert update_resp.status_code == 200, f"Update failed: {update_resp.text}"

        # Проверка
        updated = update_resp.json()

        # Проверяем все поля
        for key in updated_booking_data:
            assert updated[key] == updated_booking_data[key], f"Field {key} doesn't match"

        print(f"✅ Successfully updated booking {booking_id}")


    def test_update_patch_booking(self, auth_session, booking_data, updated_patch_booking_data):
        """
        Тест частичного обновления бронирования
        """
        # Создание
        create_resp = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_resp.status_code == 200
        booking_id = create_resp.json()["bookingid"]

        # Обновление (PATCH)
        update_patch_resp = auth_session.patch(
            f"{BASE_URL}/booking/{booking_id}",
            json=updated_patch_booking_data
        )

        assert update_patch_resp.status_code == 200, f"Update patch failed: {update_patch_resp.text}"

        # Проверка
        updated = update_patch_resp.json()

        # Проверяем все поля из фикстуры
        for key in updated_patch_booking_data:
            assert updated[key] == updated_patch_booking_data[key], f"Field {key} doesn't match"

        for key in booking_data:
            if key not in updated_patch_booking_data:
                assert updated[key] == booking_data[key], \
                    f"Field {key} changed! Should be: {booking_data[key]}, Is: {updated[key]}"

        print(f"✅ Successfully updated only 2 fields in booking {booking_id}")