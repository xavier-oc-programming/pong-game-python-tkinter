a = (1,2,3)
b = (4,5,6)

product = 0
for i in range(len(a)):
    product += a[i] * b[i]

print(f'scalar product = {product}')