// payment-service.js
// Microservicio de Pagos - Escucha órdenes y procesa pagos
const express = require('express');
const { RabbitMQService, EXCHANGES, QUEUES } = require('./rabbitmq-config');

const app = express();
app.use(express.json());

const rabbitMQ = new RabbitMQService();

// Inicializar RabbitMQ
async function initRabbitMQ() {
  await rabbitMQ.connect();
  
  // Crear y enlazar cola para órdenes creadas
  await rabbitMQ.bindQueue(QUEUES.ORDER_CREATED, EXCHANGES.ORDERS, 'order.created');
  
  // Escuchar órdenes nuevas para procesar pago
  await rabbitMQ.consume(QUEUES.ORDER_CREATED, async (message) => {
    const { orderId, userId, total } = message;
    console.log(`💰 Procesando pago para orden ${orderId} - Total: $${total}`);
    
    // Simular procesamiento de pago
    await processPayment(orderId, total);
  });
}

// Simular procesamiento de pago
async function processPayment(orderId, amount) {
  return new Promise((resolve) => {
    setTimeout(async () => {
      const paymentId = `PAY-${Date.now()}`;
      const success = Math.random() > 0.1; // 90% éxito
      
      if (success) {
        console.log(`✅ Pago exitoso: ${paymentId}`);
        
        // Publicar evento de pago exitoso
        await rabbitMQ.publish(EXCHANGES.PAYMENTS, 'payment.success', {
          orderId,
          paymentId,
          amount,
          status: 'SUCCESS',
          timestamp: new Date()
        });
        
        // Notificar al usuario
        await rabbitMQ.publish(EXCHANGES.NOTIFICATIONS, '', {
          type: 'PAYMENT_SUCCESS',
          orderId,
          paymentId,
          message: `Pago de $${amount} procesado exitosamente`
        });
        
      } else {
        console.log(`❌ Pago fallido para orden ${orderId}`);
        
        await rabbitMQ.publish(EXCHANGES.PAYMENTS, 'payment.failed', {
          orderId,
          status: 'FAILED',
          reason: 'Fondos insuficientes',
          timestamp: new Date()
        });
      }
      
      resolve();
    }, 2000); // Simular 2 segundos de procesamiento
  });
}

// Endpoint REST para consultas directas (opcional)
app.post('/payments/process', async (req, res) => {
  try {
    const { orderId, amount } = req.body;
    
    await processPayment(orderId, amount);
    
    res.json({ 
      success: true, 
      message: 'Pago en procesamiento' 
    });
  } catch (error) {
    res.status(500).json({ error: 'Error procesando pago' });
  }
});

// GET /payments/:id - Consultar estado de pago
app.get('/payments/:id', async (req, res) => {
  try {
    const { id } = req.params;
    // const payment = await getPaymentById(id);
    
    res.json({ 
      id, 
      status: 'PROCESSED',
      message: 'Pago encontrado' 
    });
  } catch (error) {
    res.status(404).json({ error: 'Pago no encontrado' });
  }
});

// Iniciar servidor
const PORT = process.env.PORT || 5004;
app.listen(PORT, async () => {
  console.log(`🚀 Payment Service running on port ${PORT}`);
  await initRabbitMQ();
});

module.exports = app;