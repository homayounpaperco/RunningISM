<script>
import {initFlowbite} from 'flowbite'
import Card from '@/components/Card'
import modal from "@/components/Modal.vue";
import Alert from "@/components/Alert.vue";
import ReportAlert from "@/components/ReportAlert.vue";
import {jsPDF} from "jspdf";
import html2canvas from 'html2canvas';
import {useToast} from "vue-toastification";
import licenseNumber from '@/components/licenseNumber.vue';


export default {
  name: "reportPage",
  components: {
    licenseNumber,
    Card,
    modal,
    Alert,
    ReportAlert
  },
  data() {
    return {
      forms: {
        shipments: {
          type: 'input',
          title: 'لیست بارنامه',
          filter: 'فیلتر',
          data: '',
          value: '',
          fields: [],
          CopyData: [],
          searchQuery: ''
        },
        sales: {
          type: 'input',
          title: 'لیست فروش',
          filter: 'فیلتر',
          data: '',
          value: '',
          fields: [],
          CopyData: [],
          searchQuery: ''
        },
        purchases: {
          type: 'input',
          title: 'لیست خرید',
          filter: 'فیلتر',
          data: '',
          value: '',
          fields: [],
          CopyData: [],
          searchQuery: ''
        },
        rawMaterial: {
          type: 'input',
          title: 'لیست مواد اولیه',
          filter: 'فیلتر',
          data: '',
          value: '',
          fields: [],
          CopyData: [],
          searchQuery: ''
        },
        products: {
          type: 'input',
          title: 'لیست محصولات',
          filter: 'فیلتر',
          data: '',
          value: '',
          fields: [],
          CopyData: [],
          searchQuery: ''
        },
        consumption: {
          type: 'input',
          title: 'لیست مصرف',
          filter: 'فیلتر',
          data: '',
          value: '',
          fields: [],
          CopyData: [],
          searchQuery: ''
        },
        alerts: {
          type: 'input',
          title: 'هشدار ها',
          filter: 'فیلتر',
          data: [],
          value: '',
          fields: ['date', 'status', 'message'],
          CopyData: [],
          searchQuery: ''
        },
      },
      filters: [
        {lable: 'یک سال اخیر', value: 'year'},
        {lable: 'یک ماه اخیر', value: 'month'},
        {lable: 'هفته اخیر', value: 'week'},
        {lable: 'امروز', value: 'day'},
      ],
      success: false,
      error: false,
      errors: [],

      // Initialize the countdown to 15 minutes (15 * 60 seconds)
      totalSeconds: 5 * 60,
      alerts: [], // Reactive property to store messages
      alertSocket: null, // WebSocket connection
      searchQuery: '',
      currentFilter: 'year', // Track current filter for pagination
      currentFilters: {
        shipments: 'year',
        sales: 'year', 
        purchases: 'year',
        rawMaterial: 'year',
        products: 'year',
        consumption: 'year',
        alerts: 'year'
      }, // Track current filter for each table
    }
  },
  computed: {
    // Format the time for display
    formattedTime() {
      const minutes = Math.floor(this.totalSeconds / 60);
      const seconds = this.totalSeconds % 60;
      return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
  },
  mounted() {
    this.toast = useToast();
    initFlowbite();
    // this.load_data()
    this.startCountdown();
    this.report_shipment('year')
    this.report_Products('year')
    this.report_Sales('year')
    this.report_Purchases('year')
    this.report_Consumption('year')
    this.report_RawMaterial('year')
    this.report_alerts('year')
    
    // Fetch unread alerts on component mount
    this.getUnreadAlerts();
    
    // Initialize WebSocket connection
    this.alertSocket = new WebSocket('ws://' + window.location.host + '/ws/alert/');
    
    // Set up message handler
    this.alertSocket.onmessage = (e) => {
      const data = JSON.parse(e.data);
      // console.log(this.forms.alerts.data);
      // console.log(data.data);
      const toastId = this.toast.warning(data.message, {
        timeout: false,
        closeOnClick: false,
        rtl: true,
        onClose: () => this.markAlertAsResolved(alert.id),
      });
      
      // this.alerts.push({
      //   id: data.data.id,
      //   message: data.message,
      //   date: data.data.date,
      //   status: data.data.status,
      //   toastId: toastId
      // });

      const toastIdCountAlert = this.toast.info(`Displayed 1 unread alerts`, {position: 'top-left',});
      this.update_alert(data.data)
    };

    // Handle WebSocket errors
    this.alertSocket.onerror = (error) => {
      console.error('WebSocket Error: ', error);
    };

  },
  beforeDestroy() {
    // Close WebSocket connection when component is destroyed
    if (this.alertSocket) {
      this.alertSocket.close();
    }
  },
  methods: {
    formatNumber(value) {
      if (value === null || value === undefined) {
        return ''; // یا هر مقدار پیش‌فرضی که می‌خواهید برای null/undefined برگردانید
      }
      return value.toString().replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
    async getUnreadAlerts() {
      try {
        const response = await this.axios.get('/myapp/api/getUnreadAlerts');
        // console.log('Unread alerts response:', response.data);
        if (response.data.status === 'success' && response.data.alerts) {
          // Display each unread alert with toast notification
          if(response.data.count != 0){
            const toastIdCountAlert = this.toast.info(`Displayed ${response.data.count} unread alerts`, {position: 'top-left',});
          }
          response.data.alerts.forEach(alert => {
            const toastId = this.toast.warning(alert.message, {
              timeout: false,
              closeOnClick: false,
              rtl: true,
              onClose: () => this.markAlertAsResolved(alert.id),
            });
            
            // Add to alerts array for display in the UI
            // this.alerts.push({
            //   id: alert.id,
            //   message: alert.message,
            //   date: alert.date,
            //   status: alert.status,
            //   toastId: toastId
            // });
          });
        }
      } catch (error) {
        console.error('Error fetching unread alerts:', error);
        this.toast.error('خطا در دریافت هشدارهای جدید', {
          timeout: 5000,
          position: 'top-right',
        });
      }
    },
    async markAlertAsResolved(alertId) {
      try {
        const response = await this.axios.post('/myapp/api/alertsResolve', {
          alert_id: alertId
        }, {
          headers: {
            'Content-Type': 'application/json',
          }
        });
        if (response.data.status === 'success') {
          console.log(`Alert ${alertId} marked as resolved`);
          // Remove the alert from the alerts array
          // this.alerts = this.alerts.filter(alert => alert.id !== alertId);
          
          // Update the alerts table data if it exists
          if (this.forms.alerts.data) {
            this.forms.alerts.data = this.forms.alerts.data.map(alert => {
              // console.log(alert.id, alertId, alert)
              if (alert.id === alertId) {
                return { ...alert, status: 'Resolved' };
              }
              return alert;
            });
          }
        }
      } catch (error) {
        console.error('Error marking alert as resolved:', error);
        this.toast.error('خطا در بروزرسانی وضعیت هشدار', {
          timeout: 5000,
          position: 'top-right',
        });
      }
    },
    update_alert(d) {
      this.forms.alerts.data.unshift(d);
    },
    async generate_excel_report(model_name) {
      console.log(model_name)
      const params = {
        'model_name': model_name,
      }
      const response = await this.axios.post('/myapp/api/generateExcelReport', {}, {
        params: params,
        responseType: 'blob',
      },)
      // Create a URL for the blob
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;

      // Suggest a filename for the downloaded file
      const filename = response.headers['content-disposition'];
      link.setAttribute('download', filename);

      // Append the link to the body
      document.body.appendChild(link);

      // Simulate click to download the file
      link.click();

      // Remove the link from the body
      document.body.removeChild(link);

      console.log(response.data)
    },
    reload() {
      window.location.reload();
    },
    countdown() {
      if (this.totalSeconds > 0) {
        // Decrement the total seconds by one
        this.totalSeconds -= 1;
      } else {
        // If the countdown has finished, refresh the page
        window.location.reload();
      }
    },
    startCountdown() {
      // Call the countdown function every second
      this.interval = setInterval(this.countdown, 1000);
    },
    select(obj) {
      this.forms.shipment_list.value = obj
    },
    clicked(k, data) {
      if (k == 'shipments') {
        this.forms.shipments.filter = data.lable
        this.report_shipment(data.value)
      }
      if (k == 'sales') {
        this.forms.sales.filter = data.lable
        this.report_Sales(data.value)
      }
      if (k == 'purchases') {
        this.forms.purchases.filter = data.lable
        this.report_Purchases(data.value)
      }
      if (k == 'rawMaterial') {
        this.forms.rawMaterial.filter = data.lable
        this.report_RawMaterial(data.value)
      }
      if (k == 'products') {
        this.forms.products.filter = data.lable
        this.report_Products(data.value)
      }
      if (k == 'consumption') {
        this.forms.consumption.filter = data.lable
        this.report_Consumption(data.value)
      }
      if (k == 'alerts') {
        this.forms.alerts.filter = data.lable
        this.report_alerts(data.value)
      }
    },
    async load_data() {
      const response = await this.axios.get('/myapp/api/loadReportData')
      console.log(response.data['data']); // Access response data
      // console.log(JSON.parse(response.data['isExists'])); // Access response data
      this.forms = response.data['data']
      // this.forms.shipment_list.data = response.data['data'].shipments.values
      // this.forms.shipment_list.fields = response.data['data'].shipments.fields
      // console.log(JSON.parse(response.data['shipment_list']))
    },
    printTable(id) {
      let table = document.getElementById(id); // Replace 'yourTableId' with your table's ID
      console.log(table)
      html2canvas(table).then(function (canvas) {
        let imgData = canvas.toDataURL('image/png');
        console.log(imgData)
        var doc = new jsPDF('p', 'mm', 'a4');
        var imgHeight = canvas.height * 210 / canvas.width;
        doc.addImage(imgData, 'PNG', 0, 0, 210, imgHeight);
        doc.save('table.pdf');
      });
    },
    async report_Sales(filter, page = 1, pageSize = 10, searchQuery = '') {
      try {
        // Store current filter for pagination
        this.currentFilters.sales = filter
        
        const params = {
          'filter': filter,
          'page': page,
          'page_size': pageSize
        }
        
        // Add search parameter if provided
        if (searchQuery) {
          params.search = searchQuery
        }
        const response = await this.axios.post('/myapp/api/reportSales', {}, {params: params})
        console.log(response.data);
        this.forms['sales'].data = response.data['values']
        this.forms['sales'].CopyData = response.data['values']
        this.forms['sales'].fields = response.data['fields']
        
        // Store pagination information
        this.forms['sales'].pagination = response.data['pagination']
      } catch (error) {
        console.error("Error fetching sales report:", error);
        this.forms['sales'].data = []
        this.forms['sales'].CopyData = []
        this.forms['sales'].pagination = null
      }
    },
    async report_Purchases(filter, page = 1, pageSize = 10, searchQuery = '') {
      try {
        // Store current filter for pagination
        this.currentFilters.purchases = filter
        
        const params = {
          'filter': filter,
          'page': page,
          'page_size': pageSize
        }
        
        // Add search parameter if provided
        if (searchQuery) {
          params.search = searchQuery
        }
        const response = await this.axios.post('/myapp/api/reportPurchases', {}, {params: params})
        console.log(response.data);
        this.forms['purchases'].data = response.data['values']
        this.forms['purchases'].CopyData = response.data['values']
        this.forms['purchases'].fields = response.data['fields']
        
        // Store pagination information
        this.forms['purchases'].pagination = response.data['pagination']
      } catch (error) {
        console.error("Error fetching purchases report:", error);
        this.forms['purchases'].data = []
        this.forms['purchases'].CopyData = []
        this.forms['purchases'].pagination = null
      }
    },
    async report_RawMaterial(filter, page = 1, pageSize = 10) {
      try {
        // Store current filter for pagination
        this.currentFilters.rawMaterial = filter
        
        const params = {
          'filter': filter,
          'page': page,
          'page_size': pageSize
        }
        const response = await this.axios.post('/myapp/api/reportRawMaterial', {}, {params: params})
        console.log(response.data);
        this.forms['rawMaterial'].data = response.data['values']
        this.forms['rawMaterial'].CopyData = response.data['values']
        this.forms['rawMaterial'].fields = response.data['fields']
        
        // Store pagination information
        this.forms['rawMaterial'].pagination = response.data['pagination']
      } catch (error) {
        console.error("Error fetching raw material report:", error);
        this.forms['rawMaterial'].data = []
        this.forms['rawMaterial'].CopyData = []
        this.forms['rawMaterial'].pagination = null
      }
    },
    async report_Products(filter, page = 1, pageSize = 10) {
      try {
        // Store current filter for pagination
        this.currentFilters.products = filter
        
        const params = {
          'filter': filter,
          'page': page,
          'page_size': pageSize
        }
        const response = await this.axios.post('/myapp/api/reportProducts', {}, {params: params})
        console.log(response.data);
        this.forms['products'].data = response.data['values']
        this.forms['products'].CopyData = response.data['values']
        this.forms['products'].fields = response.data['fields']
        
        // Store pagination information
        this.forms['products'].pagination = response.data['pagination']
      } catch (error) {
        console.error("Error fetching products report:", error);
        this.forms['products'].data = []
        this.forms['products'].CopyData = []
        this.forms['products'].pagination = null
      }
    },
    async report_Consumption(filter, page = 1, pageSize = 10) {
      try {
        // Store current filter for pagination
        this.currentFilters.consumption = filter
        
        const params = {
          'filter': filter,
          'page': page,
          'page_size': pageSize
        }
        const response = await this.axios.post('/myapp/api/reportConsumption', {}, {params: params})
        this.forms['consumption'].data = response.data['values']
        this.forms['consumption'].CopyData = response.data['values']
        this.forms['consumption'].fields = response.data['fields']
        
        // Store pagination information
        this.forms['consumption'].pagination = response.data['pagination']
      } catch (error) {
        console.error("Error fetching consumption report:", error);
        this.forms['consumption'].data = []
        this.forms['consumption'].CopyData = []
        this.forms['consumption'].pagination = null
      }
    },
    async report_shipment(filter, page = 1, pageSize = 10, searchQuery = '') {
      try {
        // Store current filter for pagination
        this.currentFilters.shipments = filter
        
        const params = {
          'filter': filter,
          'page': page,
          'page_size': pageSize
        }
        
        // Add search parameter if provided
        if (searchQuery) {
          params.search = searchQuery
        }
        const response = await this.axios.post('/myapp/api/reportShipment', {}, {params: params})

        this.forms['shipments'].data = response.data['values']
        this.forms['shipments'].CopyData = response.data['values']
        this.forms['shipments'].fields = response.data['fields']
        
        // Store pagination information
        this.forms['shipments'].pagination = response.data['pagination']

      } catch (error) {
        console.error("Error fetching shipment report:", error);
        this.forms['shipments'].data = []
        this.forms['shipments'].CopyData = []
        this.forms['shipments'].pagination = null
      }
    },
    async report_alerts(filter, page = 1, pageSize = 10) {
      try {
        // Store current filter for pagination
        this.currentFilter = filter
        
        const params = {
          'filter': filter,
          'page': page,
          'page_size': pageSize
        }
        const response = await this.axios.post('/myapp/api/reportAlert', {}, {params: params})
        console.log(response.data);
        
        // Update the data
        this.forms['alerts'].data = response.data['values']
        this.forms['alerts'].CopyData = response.data['values']
        this.forms['alerts'].fields = response.data['fields']
        
        // Store pagination information
        this.forms['alerts'].pagination = response.data['pagination']
        
        console.log(this.forms.alerts)
      } catch (error) {
        console.error("Error fetching alerts report:", error);

        this.forms['alerts'].data = []
        this.forms['alerts'].CopyData = []
        this.forms['alerts'].pagination = null
      }
    },

    // Pagination methods for alerts
    async goToPage(page) {
      if (this.forms['alerts'].pagination && page >= 1 && page <= this.forms['alerts'].pagination.total_pages) {
        await this.report_alerts(this.currentFilter, page, this.forms['alerts'].pagination.page_size)
      }
    },

    async nextPage() {
      if (this.forms['alerts'].pagination && this.forms['alerts'].pagination.has_next) {
        await this.goToPage(this.forms['alerts'].pagination.current_page + 1)
      }
    },

    async previousPage() {
      if (this.forms['alerts'].pagination && this.forms['alerts'].pagination.has_previous) {
        await this.goToPage(this.forms['alerts'].pagination.current_page - 1)
      }
    },

    async changePageSize(pageSize) {
      await this.report_alerts(this.currentFilter, 1, pageSize)
    },

    // Generic pagination methods for all tables
    async goToPageForTable(tableName, page) {
      const pagination = this.forms[tableName].pagination
      if (pagination && page >= 1 && page <= pagination.total_pages) {
        const currentFilter = this.currentFilters[tableName]
        const pageSize = pagination.page_size
        
        switch(tableName) {
          case 'shipments':
            await this.report_shipment(currentFilter, page, pageSize)
            break
          case 'sales':
            await this.report_Sales(currentFilter, page, pageSize)
            break
          case 'purchases':
            await this.report_Purchases(currentFilter, page, pageSize)
            break
          case 'rawMaterial':
            await this.report_RawMaterial(currentFilter, page, pageSize)
            break
          case 'products':
            await this.report_Products(currentFilter, page, pageSize)
            break
          case 'consumption':
            await this.report_Consumption(currentFilter, page, pageSize)
            break
          case 'alerts':
            await this.report_alerts(currentFilter, page, pageSize)
            break
        }
      }
    },

    async nextPageForTable(tableName) {
      const pagination = this.forms[tableName].pagination
      if (pagination && pagination.has_next) {
        await this.goToPageForTable(tableName, pagination.current_page + 1)
      }
    },

    async previousPageForTable(tableName) {
      const pagination = this.forms[tableName].pagination
      if (pagination && pagination.has_previous) {
        await this.goToPageForTable(tableName, pagination.current_page - 1)
      }
    },

    async changePageSizeForTable(tableName, pageSize) {
      const currentFilter = this.currentFilters[tableName]
      
      switch(tableName) {
        case 'shipments':
          await this.report_shipment(currentFilter, 1, pageSize)
          break
        case 'sales':
          await this.report_Sales(currentFilter, 1, pageSize)
          break
        case 'purchases':
          await this.report_Purchases(currentFilter, 1, pageSize)
          break
        case 'rawMaterial':
          await this.report_RawMaterial(currentFilter, 1, pageSize)
          break
        case 'products':
          await this.report_Products(currentFilter, 1, pageSize)
          break
        case 'consumption':
          await this.report_Consumption(currentFilter, 1, pageSize)
          break
        case 'alerts':
          await this.report_alerts(currentFilter, 1, pageSize)
          break
      }
    },

    // Generate page numbers for any table
    getPageNumbersForTable(tableName) {
      const pagination = this.forms[tableName].pagination
      if (!pagination) return []
      
      const current = pagination.current_page
      const total = pagination.total_pages
      const delta = 2 // Number of pages to show on each side of current page
      
      const range = []
      const rangeWithDots = []
      
      for (let i = Math.max(2, current - delta); i <= Math.min(total - 1, current + delta); i++) {
        range.push(i)
      }
      
      if (current - delta > 2) {
        rangeWithDots.push(1, '...')
      } else {
        rangeWithDots.push(1)
      }
      
      rangeWithDots.push(...range)
      
      if (current + delta < total - 1) {
        rangeWithDots.push('...', total)
      } else if (total > 1) {
        rangeWithDots.push(total)
      }
      
      return rangeWithDots
    },

    // Generate page numbers for pagination display
    getPageNumbers() {
      console.log('getPageNumbers')
      if (!this.forms.alerts.pagination) return []
      
      const current = this.forms.alerts.pagination.current_page
      const total = this.forms.alerts.pagination.total_pages
      const delta = 2 // Number of pages to show on each side of current page
      
      const range = []
      const rangeWithDots = []
      
      for (let i = Math.max(2, current - delta); i <= Math.min(total - 1, current + delta); i++) {
        range.push(i)
      }
      
      if (current - delta > 2) {
        rangeWithDots.push(1, '...')
      } else {
        rangeWithDots.push(1)
      }
      
      rangeWithDots.push(...range)
      
      if (current + delta < total - 1) {
        rangeWithDots.push('...', total)
      } else if (total > 1) {
        rangeWithDots.push(total)
      }
      
      return rangeWithDots
    },

    sortTable(tableName, column) {
      this.forms[tableName].data.sort((a, b) => {
        // Check if the column data is a number
        if (!isNaN(a[column]) && !isNaN(b[column])) {
          return a[column] - b[column];
        }
        // Check if the column data is a string
        if (typeof a[column] === 'string' && typeof b[column] === 'string') {
          // Convert both strings to lowercase for case-insensitive comparison
          const aLower = a[column].toLowerCase();
          const bLower = b[column].toLowerCase();
          if (aLower < bLower) {
            return -1;
          }
          if (aLower > bLower) {
            return 1;
          }
          return 0;
        }
        // If the data is neither a number nor a string, sort alphabetically
        if (a[column] < b[column]) {
          return -1;
        }
        if (a[column] > b[column]) {
          return 1;
        }
        return 0;
      });
    },

    reverseTable(tableName, column) {
      // Reverse the order of the data in the specified column using.reverse()
      this.forms[tableName].data = this.forms[tableName].data.map(row => {
        const reversedRow = {};
        for (const key in row) {
          reversedRow[key] = row[key];
        }
        reversedRow[column] = row[column].reverse();
        return reversedRow;
      });
    },

    filterTable(tableName) {
      const searchQuery = this.forms[tableName].searchQuery
      // If the table supports backend search (all main reports), call the report method with search
      if (["shipments", "sales", "purchases", "rawMaterial", "products", "consumption", "alerts"].includes(tableName)) {
        // Call the report method for this table with the current filter and search query
        const currentFilter = this.currentFilters[tableName]
        const pageSize = this.forms[tableName].pagination ? this.forms[tableName].pagination.page_size : 10
        switch(tableName) {
          case 'shipments':
            this.report_shipment(currentFilter, 1, pageSize, searchQuery)
            break
          case 'sales':
            this.report_Sales(currentFilter, 1, pageSize, searchQuery)
            break
          case 'purchases':
            this.report_Purchases(currentFilter, 1, pageSize, searchQuery)
            break
          case 'rawMaterial':
            this.report_RawMaterial(currentFilter, 1, pageSize, searchQuery)
            break
          case 'products':
            this.report_Products(currentFilter, 1, pageSize, searchQuery)
            break
          case 'consumption':
            this.report_Consumption(currentFilter, 1, pageSize, searchQuery)
            break
          case 'alerts':
            this.report_alerts(currentFilter, 1, pageSize, searchQuery)
            break
        }
      } else {
        // Fallback: local filtering for tables without backend search
        if (searchQuery) {
          this.forms[tableName].data = this.forms[tableName].CopyData.filter(item => {
          return Object.values(item).some(value =>
              value !== null && value !== undefined &&
                value.toString().toLowerCase().includes(searchQuery.toLowerCase())
          );
        });
      } else {
        this.forms[tableName].data = this.forms[tableName].CopyData
        }
      }
    }

  },
}
</script>

<template>

  <div>
    <teleport to="body">
      <section class="fixed inset-0 dark:bg-gray-900 z-50 overflow-y-auto">
        <div class="flex flex-col px-6 py-8 mx-auto h-screen overflow-y-auto lg:py-0 gap-4">

          <nav class="bg-white shadow">
            <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4 gap-2">
              <p class="flex flex-row items-center gap-2">
                <button @click="reload"
                  class="block w-auto rounded-lg bg-green-500 px-5 text-center text-sm font-medium text-white py-2.5 hover:bg-green-600 focus:outline-none focus:ring-4 focus:ring-green-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                  type="button">
                  بارگیری مجدد
                </button>
                {{ formattedTime }}
              </p>
            </div>
          </nav>

          <template v-for="(val, tableName) in forms">
            <div class="h-[calc(100vh-2rem)] w-full shadow-md sm:rounded-lg flex flex-col">
              <div
                class="w-full bg-white p-5 text-left rtl:text-right text-lg font-semibold text-gray-900 dark:bg-gray-800 dark:text-white flex-shrink-0">
                <div class="flex flex-row items-center justify-between gap-2">
                  <!-- Title Section -->
                  <div class="flex items-center">
                    <template v-if="tableName == 'products'">
                      <router-link to="/myapp/ProductsPage/" type="button"
                        class="font-medium text-blue-600 hover:underline dark:text-blue-500">
                        {{ val.title }}
                      </router-link>
                    </template>
                    <template v-else>
                      {{ val.title }}
                    </template>
                  </div>

                  <!-- Desktop Menu - Hidden on small screens -->
                  <div class="hidden md:flex flex-row items-center gap-2">
                    <button @click="printTable(tableName)"
                      class="block w-auto rounded-lg bg-green-500 px-5 text-center text-sm font-medium text-white py-2.5 hover:bg-green-600 focus:outline-none focus:ring-4 focus:ring-green-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                      type="button">
                      PDF
                    </button>
                    <button @click="generate_excel_report(tableName)"
                      class="block w-auto rounded-lg bg-green-500 px-5 text-center text-sm font-medium text-white py-2.5 hover:bg-green-600 focus:outline-none focus:ring-4 focus:ring-green-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                      type="button">
                      XLS
                    </button>

                    <button :id="tableName + 'Button1'" :data-dropdown-toggle="tableName+'dropdown1'"
                      class="inline-flex w-44 items-center justify-between rounded-lg bg-green-500 px-5 text-center text-sm font-medium text-white py-2.5 hover:bg-green-600 focus:outline-none focus:ring-4 focus:ring-green-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                      type="button">
                      {{ val.filter }}
                      <svg class="w-2.5 h-2.5 ms-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                        viewBox="0 0 10 6">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="m1 1 4 4 4-4" />
                      </svg>
                    </button>
                    <!-- Dropdown menu -->
                    <div :id="tableName+'dropdown1'"
                      class="z-50 hidden w-44 rounded-lg bg-white shadow divide-y divide-gray-100 dark:bg-gray-700">
                      <ul class="h-auto max-h-48 overflow-y-auto py-2 text-sm text-gray-700 dark:text-gray-200"
                        :aria-labelledby="tableName + 'Button1'">
                        <li v-for="data in filters">
                          <a @click='clicked(tableName ,data)' type="button"
                            class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">
                            {{ data.lable }}
                          </a>
                        </li>
                      </ul>
                    </div>
                    <input type="text" v-model="forms[tableName].searchQuery" @input="filterTable(tableName)"
                      class="block rounded-lg border border-gray-300 bg-gray-50 p-2 pl-10 text-sm text-gray-900 w-md focus:ring-primary-500 focus:border-primary-500 dark:placeholder-gray-400 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                      placeholder="Search" required="">
                  </div>

                  <!-- Mobile Menu Button - Visible only on small screens -->
                  <div class="md:hidden">
                    <button :id="tableName + 'MobileMenu'" :data-dropdown-toggle="tableName+'MobileDropdown'"
                      class="inline-flex items-center justify-center w-10 h-10 rounded-lg bg-green-500 text-white hover:bg-green-600 focus:outline-none focus:ring-4 focus:ring-green-300"
                      type="button">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                      </svg>
                    </button>
                    <!-- Mobile Dropdown Menu -->
                    <div :id="tableName+'MobileDropdown'"
                      class="z-50 hidden absolute right-0 mt-2 w-64 rounded-lg bg-white shadow-lg divide-y divide-gray-100 dark:bg-gray-700">
                      <div class="p-4 space-y-3">
                        <!-- PDF Button -->
                        <button @click="printTable(tableName)"
                          class="w-full text-right rounded-lg bg-green-500 px-4 py-2 text-sm font-medium text-white hover:bg-green-600 focus:outline-none focus:ring-4 focus:ring-green-300"
                          type="button">
                          PDF
                        </button>
                        <!-- XLS Button -->
                        <button @click="generate_excel_report(tableName)"
                          class="w-full text-right rounded-lg bg-green-500 px-4 py-2 text-sm font-medium text-white hover:bg-green-600 focus:outline-none focus:ring-4 focus:ring-green-300"
                          type="button">
                          XLS
                        </button>
                        <!-- Filter Button -->
                        <button :id="tableName + 'MobileFilter'" :data-dropdown-toggle="tableName+'MobileFilterDropdown'"
                          class="w-full text-right rounded-lg bg-green-500 px-4 py-2 text-sm font-medium text-white hover:bg-green-600 focus:outline-none focus:ring-4 focus:ring-green-300 flex items-center justify-between"
                          type="button">
                          {{ val.filter }}
                          <svg class="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                            viewBox="0 0 10 6">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="m1 1 4 4 4-4" />
                          </svg>
                        </button>
                        <!-- Mobile Filter Dropdown -->
                        <div :id="tableName+'MobileFilterDropdown'"
                          class="hidden mt-2 rounded-lg bg-gray-50 dark:bg-gray-600">
                          <ul class="py-2 text-sm text-gray-700 dark:text-gray-200">
                            <li v-for="data in filters">
                              <a @click='clicked(tableName ,data)' type="button"
                                class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">
                                {{ data.lable }}
                              </a>
                            </li>
                          </ul>
                        </div>
                        <!-- Search Input -->
                        <input type="text" v-model="forms[tableName].searchQuery" @input="filterTable(tableName)"
                          class="w-full rounded-lg border border-gray-300 bg-gray-50 p-2 text-sm text-gray-900 focus:ring-primary-500 focus:border-primary-500 dark:placeholder-gray-400 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                          placeholder="Search" required="">
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="flex-1 overflow-hidden flex flex-col">
                <div class="overflow-auto flex-1">
                  <table :id="tableName"
                    class="min-w-full text-left rtl:text-right text-sm text-gray-500 dark:text-gray-400">
                    <thead
                      class="bg-green-500 text-xs uppercase text-gray-100 dark:bg-gray-700 dark:text-gray-400 sticky top-0 z-10">
                      <tr>
                        <template v-for="(column ,k) in val.fields">
                          <template v-if="column !='id'">
                            <th scope="col" class="px-2 py-3" @click="sortTable(tableName, column)">
                              {{ column }}
                            </th>
                          </template>
                        </template>
                      </tr>
                    </thead>
                    <tbody class="overflow-y-auto">
                      <template v-if="val.data && val.data.length > 0">
                        <template v-for="(v, index) in val.data">
                          <tr
                            class="truncate border-b bg-white hover:bg-green-50 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-600">
                            <template v-for="(field ,k) in val.fields">
                              <template v-if="field !='id'">
                                <td class="w-4 p-4">
                                  <template v-if="field == 'license_number'">
                                    <!-- {{v[field]}} -->
                                    <licenseNumber :lic="v[field]"></licenseNumber>
                                  </template>
                                  <template v-else-if="field == 'list_of_reels'">
                                    <div class="flex items-center space-x-2 space-x-reverse order-2 sm:order-1">
                                      <select class="w-full block p-2.5 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                                        <template v-for="i in v[field].split(',')" v-if="v[field]">
                                          <option :value="i">{{i}}</option>
                                        </template>
                                      </select>
                                    </div>
                                  </template>
                                  <template v-else-if="field == 'weight1'">{{ formatNumber(v[field]) }}</template>
                                  <template v-else-if="field == 'weight2'">{{ formatNumber(v[field]) }}</template>
                                  <template v-else-if="field == 'weight2'">{{ formatNumber(v[field]) }}</template>
                                  <template v-else-if="field == 'net_weight'">{{ formatNumber(v[field]) }}</template>
                                  <template v-else-if="field == 'price_per_kg'">{{ formatNumber(v[field]) }}</template>
                                  <template v-else-if="field == 'total_price'">{{ formatNumber(v[field]) }}</template>
                                  <template v-else>
                                    {{ v[field] }}
                                  </template>
                                </td>
                              </template>
                            </template>
                          </tr>
                        </template>
                      </template>
                      <template v-else>
                        <tr class="border-b bg-white dark:border-gray-700 dark:bg-gray-800">
                          <td :colspan="val.fields.filter(f => f !== 'id').length" class="px-4 py-8 text-center text-gray-500 dark:text-gray-400">
                            <div class="flex flex-col items-center justify-center space-y-2">
                              <svg class="w-12 h-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                              </svg>
                              <span class="text-lg font-medium">هیچ داده‌ای یافت نشد</span>
                              <span class="text-sm">لطفاً فیلتر یا جستجو را تغییر دهید</span>
                            </div>
                          </td>
                        </tr>
                      </template>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- Pagination Controls for All Tables -->
              <div v-if="forms[tableName].pagination"
                class="flex flex-col sm:flex-row items-center justify-between px-4 py-3 bg-white border-t border-gray-200 dark:bg-gray-800 dark:border-gray-700 flex-shrink-0 gap-4 overflow-x-auto">
                <div class="flex items-center space-x-2 space-x-reverse min-w-max">
                  <span class="text-sm text-gray-700 dark:text-gray-300">
                    نمایش {{ (forms[tableName].pagination.current_page - 1) * forms[tableName].pagination.page_size + 1
                    }} تا
                    {{ Math.min(forms[tableName].pagination.current_page * forms[tableName].pagination.page_size,
                    forms[tableName].pagination.total_count) }}
                    از {{ forms[tableName].pagination.total_count }} مورد
                  </span>
                </div>

                <div class="flex flex-col sm:flex-row items-center gap-4 w-full sm:w-auto min-w-max">
                  <!-- Page Size Selector -->
                  <div class="flex items-center space-x-2 space-x-reverse order-2 sm:order-1">
                    <label class="text-sm text-gray-700 dark:text-gray-300 whitespace-nowrap">تعداد در صفحه:</label>
                    <select @change="changePageSizeForTable(tableName, $event.target.value)"
                      :value="forms[tableName].pagination.page_size"
                      class="w-16 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                      <option value="10">10</option>
                      <option value="20">20</option>
                      <option value="50">50</option>
                      <option value="100">100</option>
                    </select>
                  </div>

                  <!-- Navigation Section -->
                  <div class="flex items-center space-x-2 space-x-reverse order-1 sm:order-2 min-w-max">
                    <!-- Previous Button -->
                    <button @click="previousPageForTable(tableName)" :disabled="!forms[tableName].pagination.has_previous"
                      class="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white transition-colors duration-200">
                      قبلی
                    </button>

                    <!-- Page Numbers -->
                    <div class="flex items-center space-x-1 space-x-reverse overflow-x-auto">
                      <template v-for="pageNum in getPageNumbersForTable(tableName)" :key="pageNum">
                        <button v-if="pageNum !== '...'" @click="goToPageForTable(tableName, pageNum)" :class="[
                            'px-3 py-2 text-sm font-medium rounded-lg transition-colors duration-200 min-w-10 flex-shrink-0',
                            pageNum === forms[tableName].pagination.current_page
                              ? 'text-white bg-green-600 border border-green-600'
                              : 'text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white'
                          ]">
                          {{ pageNum }}
                        </button>
                        <span v-else class="px-3 py-2 text-sm text-gray-500 flex-shrink-0">...</span>
                      </template>
                    </div>

                    <!-- Next Button -->
                    <button @click="nextPageForTable(tableName)" :disabled="!forms[tableName].pagination.has_next"
                      class="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white transition-colors duration-200">
                      بعدی
                    </button>
                  </div>
                </div>
              </div>

            </div>
          </template>

        </div>
      </section>
    </teleport>
  </div>


</template>