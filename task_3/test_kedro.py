from kedro.pipeline import node, pipeline
from kedro.runner import SequentialRunner
from kedro.io import DataCatalog

# 1. Определяем обычную Python-функцию
def say_hello():
    message = "Hello, Bioinformatics World! Kedro is ready."
    print(message)
    return message

# 2. Создаем Узел (Node), оборачивая функцию
hello_node = node(
    func=say_hello, 
    inputs=None, 
    outputs="hello_output", 
    name="hello_world_node"
)

# 3. Собираем Пайплайн (Pipeline) из одного узла
hello_pipeline = pipeline([hello_node])

# 4. Запускаем пайплайн с помощью Runner
if __name__ == "__main__":
    # DataCatalog управляет входами и выходами (здесь он пустой, так как у нас нет внешних файлов)
    catalog = DataCatalog()
    runner = SequentialRunner()
    
    print("--- Запуск Kedro Pipeline ---")
    runner.run(hello_pipeline, catalog)
    print("--- Завершено ---")