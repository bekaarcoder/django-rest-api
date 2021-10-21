## Django ORM

1. **Retrieving Objects**

    ```python
    queryset = Product.objects.all()
    # Returns all the products as a queryset

    # We can iterate over queryset
    for product in queryset:
        print(product)

    product = Product.objects.get(pk=1)
    # Returns a single product object
    # If nothing exists, it throws an exception.

    products = Product.objects.filter(name="Coffee")
    # Returns a filtered queryset

    product = Product.objects.filter(pk=1).first()
    # Returns the first object from the filtered queryset

    exists = Product.objects.filter(pk=1).exists()
    # Returns a boolean
    ```

2. **Filtering Objects**

    ```python
    queryset = Product.objects.filter(price__gt=20)
    # Returns a queryset will all the products having price greater than 20.

    queryset = Products.objects.filter(collection__id=1)
    # Returns a queryset of products where collection id is 1.
    # Here collection is a model

    products = Products.objects.filter(title__contains='coffee')
    # This is case sensitive

    products = Products.objects.filter(title__icontains='coffee')
    # Case insensitive

    products = Products.objects.filter(last_update__year=2021)

    products = Products.objects.filter(description__isnull=True)
    ```

    Field lookups are similar to SQL WHERE clause. They’re specified as keyword arguments to the QuerySet methods filter(), exclude() and get()

    List of all the field lookups can be found here: https://docs.djangoproject.com/en/3.2/ref/models/querysets/#field-lookups

3. **Complex Lookups Using Q Objects**

    ```python
    # Products: inventory < 10 AND price < 20
    products = Product.objects.filter(inventory__lt=10, price__lt=20)

    # Above query can be written as mentioned below
    products = Product.objects.filter(inventory__lt=10)
                              .filter(price__lt=20)

    # Keyword argument queries are ANDed togther.
    # To execute OR statements, we can use Q Objects.
    from django.db.models import Q
    products = Product.objects.filter(
        Q(inventory__lt=10) | Q(unit_price__lt=10)
    )

    # We can also use AND using & and NOT using ~ in Q Objects
    products = Product.objects.filter(
        Q(inventory__lt=10) | ~Q(unit_price__lt=10)
    )
    ```

4. Referencing fields using F Objects

    ```python
    # Products: inventory = price
    # Using F objects, we can reference fields
    import django.db.models import F
    products = Product.objects.filter(inventory=F('price'))
    ```

5. Sorting

    ```python
    # Sorting in ASC
    queryset = Product.objects.order_by('title')

    # Soring in DESC
    queryset = Product.objects.order_by('-title')

    # Sorting by multiple fields
    queryset = Product.objects.order_by('title', 'unit_price')

    # Reverse the order of sorting
    queryset = Product.objects.order_by('title', 'unit_price').reverse()

    product = Product.objects.order_by('title')[0]
    # This will return first product object after sorting
    ```

6. Limiting Results

    ```python
    queryset = Product.objects.all()[:5]
    # Returns the 1st 5 objects as a queryset

    queryset = Product.objects.all()[5:5]
    # Returns the next 5 objects as a queryset
    ```

7. Selecting Fields to Query

    ```python
    # Select id, title, price from product
    queryset = Product.objects.values('id', 'title', 'price')

    # We can also select related fields
    queryset = Product.objects.values('id', 'title', 'price', 'collection__title')
    # This returns a dictionary

    queryset = Product.objects.values_list('id', 'title', 'price')
    # This returns a tuple

    ```

8. Deferring Fields

    ```python
    queryset = Product.objects.only('id', 'title')

    queryset = Product.objects.defer('description')
    # This will return all the fields except decsription field
    ```

9. Selecting Related Objects

    ```python
    queryset = Product.objects.select_related('collection').all()
    # This will return the products with the collection. Django creates a join between product and collection table.
    ```

10. Aggregating Objects

    ```python
    from django.db.models.aggregates import Count, Max, Min, Avg, Sum

    result = Product.objects.aggregate(Count('id'))
    # Returns the count of records as a dictionary.
    # {'id__count': 1000}

    # To change the key name in the dictionary, we can use
    result = Product.objects.aggregate(count=Count('id'))
    # {'count': 1000}

    # We can use multiple aggregates
    result = Product.objects.aggregate(count=Count('id'), min_price=Min('price'))
    ```

## Change admin password

`> python manage.py changepassword admin`

## RetrieveAPIView without a lookup_field

We need to override the `get_object`

```python
def get_object(self):
  queryset = self.get_queryset()
  obj = get_object_or_404(queryset, user=self.request.user)
  return obj
```
