

interface Product {
    brand: string,
    displayDiscountPercentage: number,
    id: number,
    name: string,
    oldPrice: number,
    price: number,
    sectionName: string,
    url: string,
    href: string
}

export default function ProductLayout({ products } : { products : Product[] }) {
    return (
        <div className="bg-white flex justify-center w-full">
        <div className="mx-auto max-w-2xl px-4 py-16 sm:px-6 sm:py-24 lg:max-w-7xl lg:px-8">
            <h2 className="text-2xl font-bold tracking-tight text-gray-900">Customers also purchased</h2>

            <div className="mt-6 grid grid-cols-1 gap-x-6 gap-y-10 sm:grid-cols-2 lg:grid-cols-4 xl:gap-x-8">
            {products.map((product) => (
                <div key={product.id} className="group relative">
                <img
                    alt={product.name}
                    src={product.url}
                    className="aspect-square w-full rounded-md bg-gray-200 object-cover group-hover:opacity-75 lg:aspect-auto lg:h-80"
                />
                <div className="mt-4 flex flex-col justify-between">
                    <div>
                    <h3 className="text-sm text-gray-700">
                        <a href={product.href}>
                        <span aria-hidden="true" className="absolute inset-0" />
                        {product.name}
                        </a>
                    </h3>
                    </div>
                    <div className="flex gap-4">
                        <div className="text-sm font-medium text-red-900">€ {product.price}</div>
                        <div className="text-sm font-medium text-gray-900 line-through">€ {product.oldPrice}</div>
                    </div>
                </div>
                </div>
            ))}
            </div>
        </div>
        </div>
    )
}