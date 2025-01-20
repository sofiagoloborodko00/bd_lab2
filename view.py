class View:
    def show_categories(self, categories):
        print("Categories:")
        for category in categories:
            print(f"ID: {category[0]}, Name: {category[1]}")

    def show_sellers(self, sellers):
        print("Sellers:")
        for seller in sellers:
            print(f"ID: {seller[0]}, Name: {seller[1]}, Number: {seller[2]}")

    def show_products(self, products):
        print("Products:")
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Category ID: {product[2]}, Seller ID: {product[3]}")

    def get_category_input(self):
        return input("Enter category name: ")

    def get_update_category_input(self):
        category_id = int(input("Enter category ID to update: "))
        name = input("Enter new category name: ")
        return category_id, name

    def get_category_id(self):
        return int(input("Enter category ID: "))

    def get_seller_input(self):
        name = input("Enter seller name: ")
        number = int(input("Enter seller number: "))
        return name, number

    def get_update_seller_input(self):
        seller_id = int(input("Enter seller ID to update: "))
        name = input("Enter new seller name: ")
        number = int(input("Enter new seller number: "))
        return seller_id, name, number

    def get_seller_id(self):
        return int(input("Enter seller ID: "))

    def get_product_input(self):
        name = input("Enter product name: ")
        category_id = int(input("Enter category ID: "))
        seller_id = int(input("Enter seller ID: "))
        return name, category_id, seller_id

    def get_update_product_input(self):
        product_id = int(input("Enter product ID to update: "))
        name = input("Enter new product name: ")
        category_id = int(input("Enter new category ID: "))
        seller_id = int(input("Enter new seller ID: "))
        return product_id, name, category_id, seller_id

    def get_product_id(self):
        return int(input("Enter product ID: "))

    def show_message(self, message):
        print(message)
    
    def show_query_results(self, results, execution_time):
        print("Query Results:")
        for row in results:
            print(row)
        print(f"Execution Time: {execution_time:.2f} ms")
