import uuid
from app.core.database import SessionLocal
from app.models.category import Category
from app.models.product import Product

CATEGORIES = [
    {"name": "Eletrônicos", "description": "Smartphones, tablets, notebooks e acessórios"},
    {"name": "Periféricos", "description": "Teclados, mouses, headsets e monitores"},
    {"name": "Armazenamento", "description": "SSDs, HDDs, pendrives e cartões de memória"},
    {"name": "Redes", "description": "Roteadores, switches e cabos de rede"},
    {"name": "Acessórios", "description": "Capas, carregadores, cabos e suportes"},
]

PRODUCTS = [
    # Eletrônicos
    {"name": "iPhone 15 Pro", "description": "Apple iPhone 15 Pro 256GB Titânio", "price": 8999.99, "stock": 15, "category": "Eletrônicos"},
    {"name": "Samsung Galaxy S24", "description": "Samsung Galaxy S24 Ultra 512GB", "price": 6799.00, "stock": 8, "category": "Eletrônicos"},
    {"name": "MacBook Air M3", "description": "Apple MacBook Air 13\" M3 16GB 512GB", "price": 12499.00, "stock": 5, "category": "Eletrônicos"},
    {"name": "iPad Pro 12.9\"", "description": "Apple iPad Pro M4 12.9\" 256GB Wi-Fi", "price": 9299.00, "stock": 0, "category": "Eletrônicos"},
    {"name": "Dell XPS 15", "description": "Dell XPS 15 Intel Core i7 16GB 512GB SSD", "price": 9999.90, "stock": 3, "category": "Eletrônicos"},
    # Periféricos
    {"name": "Teclado Mecânico Keychron K2", "description": "Teclado mecânico compacto 75% com switch Brown", "price": 549.00, "stock": 22, "category": "Periféricos"},
    {"name": "Mouse Logitech MX Master 3", "description": "Mouse sem fio ergonômico para produtividade", "price": 699.90, "stock": 18, "category": "Periféricos"},
    {"name": "Headset Sony WH-1000XM5", "description": "Fone de ouvido com cancelamento de ruído", "price": 1799.00, "stock": 7, "category": "Periféricos"},
    {"name": "Monitor LG UltraWide 34\"", "description": "Monitor ultrawide 34\" 3440x1440 144Hz IPS", "price": 3299.00, "stock": 4, "category": "Periféricos"},
    {"name": "Webcam Logitech StreamCam", "description": "Webcam Full HD 1080p 60fps USB-C", "price": 849.90, "stock": 9, "category": "Periféricos"},
    # Armazenamento
    {"name": "SSD Samsung 970 EVO 1TB", "description": "SSD NVMe M.2 1TB até 3500MB/s leitura", "price": 499.00, "stock": 30, "category": "Armazenamento"},
    {"name": "SSD Externo WD 2TB", "description": "SSD portátil USB-C 2TB até 1050MB/s", "price": 679.90, "stock": 6, "category": "Armazenamento"},
    {"name": "Pendrive Kingston 64GB", "description": "Pendrive USB 3.2 64GB 200MB/s", "price": 59.90, "stock": 50, "category": "Armazenamento"},
    {"name": "HD Externo Seagate 4TB", "description": "HD externo portátil 4TB USB 3.0", "price": 399.90, "stock": 2, "category": "Armazenamento"},
    # Redes
    {"name": "Roteador TP-Link AX3000", "description": "Roteador Wi-Fi 6 dual band AX3000", "price": 499.90, "stock": 11, "category": "Redes"},
    {"name": "Switch Cisco 8 portas", "description": "Switch gerenciável 8 portas Gigabit PoE", "price": 1199.00, "stock": 0, "category": "Redes"},
    {"name": "Cabo de Rede Cat6 10m", "description": "Cabo de rede Cat6 blindado 10 metros", "price": 39.90, "stock": 85, "category": "Redes"},
    # Acessórios
    {"name": "Suporte para Notebook Vertical", "description": "Suporte duplo ajustável em alumínio", "price": 189.90, "stock": 25, "category": "Acessórios"},
    {"name": "Carregador USB-C 65W", "description": "Carregador GaN 65W 3 portas USB-C/A", "price": 229.90, "stock": 1, "category": "Acessórios"},
    {"name": "Hub USB-C 7 em 1", "description": "Hub USB-C com HDMI 4K, USB 3.0, SD, PD 100W", "price": 319.90, "stock": 13, "category": "Acessórios"},
]


def run():
    db = SessionLocal()
    try:
        existing_categories = db.query(Category).count()
        existing_products = db.query(Product).count()

        if existing_categories > 0 or existing_products > 0:
            print(f"Banco já possui dados ({existing_categories} categorias, {existing_products} produtos). Seed ignorado.")
            return

        category_map: dict[str, str] = {}
        for cat_data in CATEGORIES:
            cat = Category(id=str(uuid.uuid4()), **cat_data)
            db.add(cat)
            db.flush()
            category_map[cat.name] = cat.id
            print(f"  ✓ Categoria: {cat.name}")

        for prod_data in PRODUCTS:
            cat_name = prod_data.pop("category")
            prod = Product(
                id=str(uuid.uuid4()),
                category_id=category_map.get(cat_name),
                **prod_data,
            )
            db.add(prod)
            print(f"  ✓ Produto: {prod.name} (estoque: {prod.stock})")

        db.commit()
        print(f"\n✅ Seed concluído: {len(CATEGORIES)} categorias, {len(PRODUCTS)} produtos.")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro no seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run()
