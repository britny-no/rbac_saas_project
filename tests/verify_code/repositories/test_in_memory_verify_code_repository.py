import pytest
import unittest
from time import sleep
from unittest.mock import MagicMock
from fastapi import HTTPException

from app.verify_code.repositories import InMemoryVerifyCodeRepository

class TestInMemoryVerifyCodeRepository(unittest.TestCase):

    def setUp(self):
        self.repo = InMemoryVerifyCodeRepository(max_cache_size=1, ttl_seconds=1)


    @pytest.mark.description("저장 성공")
    def test_save_success(self):
        # Given
        return_value = "123456"
        self.repo._generate_random_number = MagicMock(return_value=return_value)

        # When
        result = self.repo.save("test_key")

        # Then
        self.assertEqual(result, return_value)

    @pytest.mark.description("조회 성공")
    def test_get_success(self):
        # Given
        key = 'test_key_1'
        return_value = "123456"
        self.repo._generate_random_number = MagicMock(return_value=return_value)

        # When
        value = self.repo.save(key)
        result = self.repo.get(key)

        # Then
        self.assertEqual(result, value)

    @pytest.mark.description("존재하지 않는 키일시 예외 뱉기")
    def test_get_non_existent_key(self):
        # Given

        # When
        with self.assertRaises(HTTPException) as exc_info:
            result = self.repo.get('non_existent_key')

        # Then
        assert exc_info.exception.status_code == 400
        assert exc_info.exception.detail == "no value"

if __name__ == "__main__":
    unittest.main()
