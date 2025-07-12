<template>
  <div class="button-container">
    <router-link to="/myapp/invoice/havaleh" class="btn btn-primary">حواله</router-link>
    <router-link to="/myapp/invoice/sales_order" class="btn btn-secondary">فروش</router-link>
  </div>
</template>

<script>
export default {
  name: 'Invoice',
  mounted() {
    document.title = 'Invoice System';
  },
}
</script>

<style scoped>
@font-face {
  font-family: 'BNazanin';
  src: url('../assets/fonts/BNazanin.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

.button-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  gap: 20px;
}

.btn {
  margin: 5px;
  padding: 15px 40px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  font-family: 'BNazanin', Arial, sans-serif;
  font-size: 1.2em;
  transition: all 0.3s ease;
  min-width: 150px;
  text-align: center;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}
</style>
