<script>

import html2canvas from "html2canvas";
import { jsPDF } from "jspdf";

export default {
  name: 'OutgoingRemittance',
  data() {
    return {
      // data: null
      data: {
      customer_name:'customer_name',
      license_number:'71ق-78-989',
      list_of_reels:'list_of_reels',
      invoice_number:'28',
      net_weight:'12200',
      quantity:'240',
      quality:'130',
      width:'130',
      total_price:'total_price',
      material_type:'material_type',
      material_name:'کاغذ سفید لیزر درجه 1',
      driver_name:'آقای رضا اکبرزاده',
      date:'1404/02/03',
      outgoing_product_data: [],
  }
    }
  },
  mounted() {
    // Get data from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const dataParam = urlParams.get('data');
    
    if (dataParam) {
      try {
        this.data = JSON.parse(decodeURIComponent(dataParam));
        console.log('OutgoingRemittance Data received:', this.data);
      } catch (error) {
        console.error('Error parsing data:', error);
      }
    } else {
      console.log('No data received');
    }

  },
  methods: {
    
    printTable() {
      // The ID now points to the main div container
      let invoiceContainer = document.getElementById("OutgoingRemittanceDiv");
      if (!invoiceContainer) {
        console.error("Invoice container not found!");
        return;
      }

      // Configure html2canvas with better settings for A4 printing
      html2canvas(invoiceContainer, { 
        scale: 2,
        useCORS: true,
        allowTaint: true,
        backgroundColor: '#ffffff',
        width: invoiceContainer.scrollWidth,
        height: invoiceContainer.scrollHeight
      }).then(function (canvas) {
        let imgData = canvas.toDataURL("image/png");
        var doc = new jsPDF("p", "mm", "a4");
        
        // A4 dimensions in mm
        var pageWidth = 210;
        var pageHeight = 297;
        
        // Calculate scaling to fit content properly on A4
        var imgWidth = pageWidth - 20; // Leave 10mm margin on each side
        var imgHeight = (canvas.height * imgWidth) / canvas.width;
        
        // If content is taller than page, we'll need multiple pages
        if (imgHeight <= pageHeight - 20) {
          // Content fits on one page
          doc.addImage(imgData, "PNG", 10, 10, imgWidth, imgHeight);
        } else {
          // Content needs multiple pages
          var heightLeft = imgHeight;
          var position = 10; // Start with 10mm top margin
          
          // Add first page
          doc.addImage(imgData, "PNG", 10, position, imgWidth, imgHeight);
          heightLeft -= (pageHeight - 20); // Subtract available page height
          
          // Add additional pages if needed
          while (heightLeft > 0) {
            position = heightLeft - imgHeight + 10; // Adjust position for new page
            doc.addPage();
            doc.addImage(imgData, "PNG", 10, position, imgWidth, imgHeight);
            heightLeft -= (pageHeight - 20);
          }
        }
        
        doc.save("OutgoingRemittance.pdf");
      });
    },
  },
}
</script>

<template>
  
  <div>
    <teleport to="body">
      <section class="fixed inset-0 bg-gray-50 dark:bg-gray-900 z-50 overflow-y-auto">
        <section id="OutgoingRemittanceDiv" class="bg-white p-8 min-h-screen flex flex-col items-center" style="width: 210mm; max-width: 210mm; margin: 0 auto;">
          <!-- Outgoing Remittance Document (No table tag, only divs + Tailwind) -->
          <div class="w-full p-4" style="max-width: 190mm;">
            <!-- Header -->
            <div class="flex items-center justify-between mb-4">
              <div class="flex-1 text-center">
                <div class="font-bold text-xl">شرکت صنایع تولیدی کاغذ و مقوای همایون</div>
                <div class="px-2 py-1 mt-1 font-bold text-lg">حواله خروج از انبار</div>
              </div>
              <div class="w-16"></div>
              
              <div class="flex items-center space-x-2">
                <img src="@/assets/logo_howmayon.png" alt="Homayoun Logo" class="w-16 h-16 object-contain" />
              </div>
            </div>

            <!-- Date/Serial -->
            <div class="flex justify-between text-sm mb-4">
              <div class="flex space-x-2 rtl:space-x-reverse">
                <span>تاریخ ارسال :</span>
                <span>{{data.date}}</span>
              </div>
              <div class="flex space-x-2 rtl:space-x-reverse">
                <span>شماره سریال :</span>
                <span>{{ data.invoice_number }}</span>
              </div>
            </div>

            <!-- Table Header -->
            <div class="flex bg-gray-300 border-b border border-black font-bold text-sm">
              <div class="w-1/12 p-2 border-l border-black text-center">ردیف</div>
              <div class="w-3/12 p-2 border-l border-black text-center">نام کالا و مشخصات کالا</div>
              <div class="w-1/12 p-2 border-l border-black text-center">گرماژ</div>
              <div class="w-2/12 p-2 border-l border-black text-center">عرض کاغذ</div>
              <div class="w-2/12 p-2 border-l border-black text-center">نام خریدار</div>
              <div class="w-2/12 p-2 border-l border-black text-center">تعداد / مقدار</div>
              <div class="w-1/12 p-2 border-black text-center">وزن کالا</div>
            </div>
            
            <!-- Table Row -->
            <template v-for="(row, index) in data.outgoing_product_data">
            <div class="flex border-x border-b border-black text-sm">
              <div class="w-1/12 p-2 border-l border-black text-center">{{ index }}</div>
              <div class="w-3/12 p-2 border-l border-black text-center">{{ row.profile_name }}</div>
              <div class="w-1/12 p-2 border-l border-black text-center">{{ row.gsm }}</div>
              <div class="w-2/12 p-2 border-l border-black text-center">{{data.width}}</div>
              <div class="w-2/12 p-2 border-l border-black text-center">{{ data.customer_name }}</div>
              <div class="w-2/12 p-2 border-l border-black text-center">{{data.quantity}}</div>
              <div class="w-1/12 p-2 border-black text-center">{{ data.net_weight }}</div>
            </div>
            </template>
            <!-- Table Row: Total -->
            <div class="flex border-x border-b border-black font-bold text-sm">
              <div class="w-2/12 p-2 border-l border-black text-center">ملاحضات</div>
              <div class="flex gap-1 w-7/12 p-2 border-l border-black text-center justify-center items-center">
              <span>{{ data.driver_name }} </span>
              <span>{{ data.license_number }}</span>
              </div>
              <div class="w-2/12 p-2 border-l border-black text-center">جمع</div>
              <div class="w-1/12 p-2 border-black text-center">?</div>
            </div>


            <!-- Signatures -->
            <div class="flex justify-between text-sm mt-8 mb-4">
              <div class="flex-1 text-center">حسابداری</div>
              <div class="flex-1 text-center">انبارداری</div>
              <div class="flex-1 text-center">مدیر فروش</div>
              <div class="flex-1 text-center">مدیریت کارخانه</div>
              <div class="flex-1 text-center">تحویل گیرنده</div>
            </div>

            <!-- Footer -->
            <div class="flex text-sm mt-6 w-1/2">
              <div class="flex-3 text-right">بار صحیح و سالم تحویل این جانب</div>
              <div class="flex-1 text-left">گردید.</div>
            </div>
          </div>
        </section>
        
        <div class="p-8 min-h-screen flex flex-col items-center">
          <div v-if="data" class="mb-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded">
            <h3 class="font-bold">داده‌های دریافتی:</h3>
            <pre class="text-sm mt-2">{{ JSON.stringify(data, null, 2) }}</pre>
          </div>
          <button @click="printTable" class="mt-6 px-6 py-3 bg-blue-600 text-white font-bold rounded-lg shadow-md hover:bg-blue-700 transition duration-300">
            چاپ حواله خروج (PDF)
          </button>
        </div>
      </section>
    </teleport>
  </div>
</template>