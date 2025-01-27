async def get_empty_category_message(value: str) -> str:
    messages = {
        "regulatory_document": "Список нормативных документов пуст",
        "document_for_military_registration": "Список документов для воинского учета пуст",
        "alternative_civilian_service_document": "Список документов альтернативной гражданской службы пуст",
        "contract_service_document": "Список документов контрактной службы пуст",
        "students": "Список студентов пуст",
        "gallery": "Галерея пуста",
        "patriotic_education": "Список материалов по патриотическому воспитанию пуст",
        "events": "Список событий пуст",
        "military_training_camps": "Список военных сборов пуст",
        "addresses_and_links": "Список адресов и ссылок пуст",
        "contacts": "Список контактов пуст",
    }
    return messages.get(value, "Категория не найдена")
