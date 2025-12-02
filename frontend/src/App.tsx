import React, { useEffect, useState } from "react";

type Product = {
  id: number;
  name: string;
  price: number;
  stock: number;
};

export function App() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);

  async function loadProducts() {
    setLoading(true);
    try {
      const res = await fetch("/api/catalog/products");
      const data = await res.json();
      setProducts(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadProducts();
  }, []);

  async function createOrder(id: number) {
    await fetch("/api/orders/orders", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ product_id: id, quantity: 1 })
    });
    alert("Pedido enviado para a fila!");
  }

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Sistema de Catálogo e Pedidos</h1>
      <button onClick={loadProducts} disabled={loading}>
        {loading ? "Carregando..." : "Recarregar produtos"}
      </button>
      <ul>
        {products.map((p) => (
          <li key={p.id} style={{ marginTop: "1rem" }}>
            <strong>{p.name}</strong> - R$ {p.price.toFixed(2)} (Estoque: {p.stock})
            <button style={{ marginLeft: "1rem" }} onClick={() => createOrder(p.id)}>
              Fazer pedido
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
