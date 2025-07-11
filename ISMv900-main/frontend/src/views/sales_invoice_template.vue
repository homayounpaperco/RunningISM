<script>
import html2canvas from "html2canvas";
import { jsPDF } from "jspdf";

export default {
  name: "sales_invoice_template",
  data() {
    return {
      // Data extracted from the PDF
      seller: {
        name: "شرکت صنایع تولیدی کاغذ و مقوای همایون",
        economicCode: "14012603703",
        postalCode: "3364146586",
        address:
          "کیلومتر ۱۵ جاده قدیم کرج - قزوین خیابان مرغک خیابان صنعت دومین کارخانه سمت چپ",
        registrationNumber: "140300459",
        nationalId: "14012603703", // Assuming national ID is the same as economic code based on the PDF layout
        phoneFax: "026-44383368",
      },
      buyer: {
        name: "شرکت صنایع بسته بندی سهیل البرز ایرانیان",
        economicCode: "14007172415",
        postalCode: "3451168795",
        address: "قزوین بوئین زهرا خیابان اداره آب کوچه سروناز",
        registrationNumber: "", // Not provided in PDF
        nationalId: "14007172415", // Assuming national ID is the same as economic code based on the PDF layout
        phoneFax: "", // Not provided in PDF
      },
      invoice: {
        number: "12345", // Example invoice number
        date: "1403/10/04",
      },
      products: [
        {
          row: 1,
          code: 1005,
          description: "کاغذ تست لاینر گرماژ 130 عرض 250", // Corrected based on reading
          quantity: 22680,
          unit: "کیلو",
          unitPrice: 200000,
          totalAmount: 4536000000, // Calculated: 22680 * 200000
          discountAmount: 0,
          totalAfterDiscount: 4536000000,
          taxAmount: 453600000, // 10% of totalAfterDiscount
          totalWithTax: 4989600000, // totalAfterDiscount + taxAmount
        },
        // Add more products for demonstration if needed
        {
          row: 2,
          code: 1006,
          description: "مقوا پشت طوسی گرماژ 200",
          quantity: 10000,
          unit: "کیلو",
          unitPrice: 150000,
          totalAmount: 1500000000,
          discountAmount: 0,
          totalAfterDiscount: 1500000000,
          taxAmount: 150000000,
          totalWithTax: 1650000000,
        },
      ],
      summary: {
        totalAmount: 0, // Will be calculated
        totalTax: 0, // Will be calculated
        grandTotal: 0, // Will be calculated
        grandTotalInWords: "", // Will be generated
      },
    };
  },
  created() {
    this.calculateSummary();
  },
  methods: {
    calculateSummary() {
      let totalAmount = 0;
      let totalTax = 0;
      let grandTotal = 0;

      this.products.forEach(product => {
        totalAmount += product.totalAmount;
        totalTax += product.taxAmount;
        grandTotal += product.totalWithTax;
      });

      this.summary.totalAmount = totalAmount;
      this.summary.totalTax = totalTax;
      this.summary.grandTotal = grandTotal;
      this.summary.grandTotalInWords = this.numberToWords(grandTotal);
    },
    printTable() {
      // The ID now points to the main div container
      let invoiceContainer = document.getElementById("SalesInvoiceDiv");
      if (!invoiceContainer) {
        console.error("Invoice container not found!");
        return;
      }

      html2canvas(invoiceContainer, { scale: 2 }).then(function (canvas) {
        let imgData = canvas.toDataURL("image/png");
        var doc = new jsPDF("p", "mm", "a4");
        var imgWidth = 210; // A4 width in mm
        var pageHeight = 297; // A4 height in mm
        var imgHeight = (canvas.height * imgWidth) / canvas.width;
        var heightLeft = imgHeight;
        var position = 0;

        doc.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;

        while (heightLeft >= 0) {
          position = heightLeft - imgHeight;
          doc.addPage();
          doc.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
          heightLeft -= pageHeight;
        }
        doc.save("sales_invoice.pdf");
      });
    },
    async generate_excel_report(model_name) {
      console.log(model_name);
      const params = {
        model_name: model_name,
      };
      const response = await this.axios.post(
        "/myapp/api/generateExcelReport",
        {},
        {
          params: params,
          responseType: "blob",
        }
      );
      // Create a URL for the blob
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;

      // Suggest a filename for the downloaded file
      const filename = response.headers["content-disposition"];
      link.setAttribute("download", filename);

      // Append the link to the body
      document.body.appendChild(link);

      // Simulate click to download the file
      link.click();

      // Remove the link from the body
      document.body.removeChild(link);

      console.log(response.data);
    },
    // Helper function to format currency
    formatCurrency(value) {
      if (value === undefined || value === null) {
        return "";
      }
      // Format with commas and append currency unit if needed (e.g., ' ریال')
      return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
    // Simple number to words converter for Persian (for demonstration)
    numberToWords(num) {
      const units = ["", "یک", "دو", "سه", "چهار", "پنج", "شش", "هفت", "هشت", "نه"];
      const tens = ["", "ده", "بیست", "سی", "چهل", "پنجاه", "شصت", "هفتاد", "هشتاد", "نود"];
      const teens = ["ده", "یازده", "دوازده", "سیزده", "چهارده", "پانزده", "شانزده", "هفده", "هجده", "نوزده"];
      const hundreds = ["", "صد", "دویست", "سیصد", "چهارصد", "پانصد", "ششصد", "هفتصد", "هشتصد", "نهصد"];
      const thousands = ["", "هزار", "میلیون", "میلیارد", "تریلیون"];

      if (num === 0) return "صفر";

      function convertLessThanThousand(n) {
        let result = "";
        if (n >= 100) {
          result += hundreds[Math.floor(n / 100)];
          n %= 100;
          if (n > 0) result += " و ";
        }
        if (n >= 20) {
          result += tens[Math.floor(n / 10)];
          n %= 10;
          if (n > 0) result += " و ";
        } else if (n >= 10) {
          result += teens[n - 10];
          n = 0;
        }
        if (n > 0) {
          result += units[n];
        }
        return result;
      }

      let parts = [];
      let i = 0;
      while (num > 0) {
        let chunk = num % 1000;
        if (chunk > 0) {
          let chunkWords = convertLessThanThousand(chunk);
          if (thousands[i]) {
            chunkWords += " " + thousands[i];
          }
          parts.unshift(chunkWords);
        }
        num = Math.floor(num / 1000);
        i++;
      }
      return parts.join(" و ");
    }
  },
};
</script>

<template>
  <div>
    <teleport to="body">
      <section class="fixed inset-0 bg-gray-50 dark:bg-gray-900 z-50 overflow-y-auto">
        <section id="SalesInvoiceDiv"  class="bg-white p-8 min-h-screen flex flex-col items-center">
        
          <!-- Title Row -->
          <div class="flex justify-center items-center text-2xl font-bold pb-12">
            صورت حساب فروش کالا
          </div>
          <!-- Main container for the invoice, replacing the table -->
          <div dir="rtl" class="border border-black text-sm mb-6 w-full max-w-5xl overflow-hidden">

            <!-- Seller Info Header and Invoice Number/Date -->
            <div class="grid grid-cols-12 border-b border-black">
              <div class="col-span-9 border-l border-black">

                <div class="col-span-9 flex items-center justify-center p-2 text-black font-bold border-b border-black bg-gray-300">
                  مشخصات فروشنده
                </div>
                <!-- Seller Info Details -->
                  
                <div class="grid grid-cols-12 border-b border-black">
                  <div class="col-span-3 flex flex-col p-2 border-l border-black">
                    <div class="font-bold text-right">نام شخص حقیقی/حقوقی:</div>
                    <div class="text-right">{{ buyer.name }}</div>
                  </div>
                  <div class="col-span-3 flex flex-col p-2 border-l border-black">
                    <div class="font-bold text-right">کد اقتصادی:</div>
                    <div class="text-right">{{ buyer.economicCode }}</div>
                  </div>
                  <div class="col-span-3 flex flex-col p-2 border-l border-black">
                    <div class="font-bold text-right">شماره ثبت:</div>
                    <div class="text-right">{{ buyer.registrationNumber }}</div>
                  </div>
                  <div class="col-span-3 flex flex-col p-2">
                    <div class="font-bold text-right">شناسه ملی:</div>
                    <div class="text-right">{{ buyer.nationalId }}</div>
                  </div>
                </div>

                <div class="grid grid-cols-12">
                  <div class="col-span-6 flex flex-col p-2 border-l border-black">
                    <div class="font-bold text-right">نشانی:</div>
                    <div class="text-right">{{ buyer.address }}</div>
                  </div>
                  <div class="col-span-3 flex flex-col p-2 border-l border-black">
                    <div class="font-bold text-right">کد پستی:</div>
                    <div class="text-right">{{ buyer.postalCode }}</div>
                  </div>
                  <div class="col-span-3 flex flex-col p-2">
                    <div class="font-bold text-right">تلفن/نمابر:</div>
                    <div class="text-right">{{ buyer.phoneFax }}</div>
                  </div>
                </div> 
              </div>
              
              <div class="grid grid-cols-6 col-span-3 ">
                  <div class="col-span-6 flex flex-col p-2 border-b border-black">
                    <div class="font-bold text-right">شماره فاکتور:</div>
                    <div class="text-right">{{ invoice.number }}</div>
                  </div>
                  <div class="flex flex-col p-2">
                    <div class="font-bold text-right">تاریخ:</div>
                    <div class="text-right">{{ invoice.date }}</div>
                  </div>
                </div> 
            </div>
           
            <!-- Buyer Info Header -->
            <div class="flex justify-center items-center font-bold p-2 border-b border-black bg-gray-300">
              مشخصات خریدار
            </div>

            <!-- Buyer Info Details -->
            <div class="grid grid-cols-12 border-b border-black">
              <div class="col-span-3 flex flex-col p-2 border-l border-black">
                <div class="font-bold text-right">نام شخص حقیقی/حقوقی:</div>
                <div class="text-right">{{ buyer.name }}</div>
              </div>
              <div class="col-span-3 flex flex-col p-2 border-l border-black">
                <div class="font-bold text-right">کد اقتصادی:</div>
                <div class="text-right">{{ buyer.economicCode }}</div>
              </div>
              <div class="col-span-3 flex flex-col p-2 border-l border-black">
                <div class="font-bold text-right">شماره ثبت:</div>
                <div class="text-right">{{ buyer.registrationNumber }}</div>
              </div>
              <div class="col-span-3 flex flex-col p-2">
                <div class="font-bold text-right">شناسه ملی:</div>
                <div class="text-right">{{ buyer.nationalId }}</div>
              </div>
            </div>

            <div class="grid grid-cols-12 border-b border-black">
              <div class="col-span-6 flex flex-col p-2 border-l border-black">
                <div class="font-bold text-right">نشانی:</div>
                <div class="text-right">{{ buyer.address }}</div>
              </div>
              <div class="col-span-3 flex flex-col p-2 border-l border-black">
                <div class="font-bold text-right">کد پستی:</div>
                <div class="text-right">{{ buyer.postalCode }}</div>
              </div>
              <div class="col-span-3 flex flex-col p-2">
                <div class="font-bold text-right">تلفن/نمابر:</div>
                <div class="text-right">{{ buyer.phoneFax }}</div>
              </div>
            </div>

            <!-- Products Header -->
            <div class="flex justify-center items-center font-bold p-4 border-b border-black">
              مشخصات کالا
            </div>

            <!-- Products Table Header -->
            <div class="grid grid-cols-12 bg-gray-300 font-bold text-center border-b border-black">
              <div class="col-span-1 p-2 border-l border-black">ردیف</div>
              <div class="col-span-1 p-2 border-l border-black">کد کالا</div>
              <div class="col-span-2 p-2 border-l border-black">شرح کالا یا خدمت</div>
              <div class="col-span-1 p-2 border-l border-black">مقدار</div>
              <div class="col-span-1 p-2 border-l border-black">واحد</div>
              <div class="col-span-1 p-2 border-l border-black">قیمت واحد</div>
              <div class="col-span-1 p-2 border-l border-black">مبلغ کل</div>
              <div class="col-span-1 p-2 border-l border-black">مبلغ تخفیف</div>
              <div class="col-span-1 p-2 border-l border-black">مبلغ کل پس از تخفیف</div>
              <div class="col-span-1 p-2 border-l border-black">جمع مالیات و عوارض 10%</div>
              <div class="col-span-1 p-2">جمع مبلغ کل و مالیات</div>
            </div>

            <!-- Products Data -->
            <div v-for="(product, index) in products" :key="index" class="grid grid-cols-12 text-center border-b border-black">
              <div class="col-span-1 p-1 border-l border-black">{{ product.row }}</div>
              <div class="col-span-1 p-1 border-l border-black">{{ product.code }}</div>
              <div class="col-span-2 p-1 border-l border-black">{{ product.description }}</div>
              <div class="col-span-1 p-1 border-l border-black">{{ product.quantity }}</div>
              <div class="col-span-1 p-1 border-l border-black">{{ product.unit }}</div>
              <div class="col-span-1 p-1 border-l border-black text-right">{{ formatCurrency(product.unitPrice) }}</div>
              <div class="col-span-1 p-1 border-l border-black text-right">{{ formatCurrency(product.totalAmount) }}</div>
              <div class="col-span-1 p-1 border-l border-black text-right">{{ formatCurrency(product.discountAmount) }}</div>
              <div class="col-span-1 p-1 border-l border-black text-right">{{ formatCurrency(product.totalAfterDiscount) }}</div>
              <div class="col-span-1 p-1 border-l border-black text-right">{{ formatCurrency(product.taxAmount) }}</div>
              <div class="col-span-1 p-1 text-right">{{ formatCurrency(product.totalWithTax) }}</div>
            </div>

            <!-- Empty Rows for Additional Products (replicated with divs) -->
            <div v-for="i in 4" :key="'empty-row-' + i" class="grid grid-cols-12 border-b border-black">
              <div class="col-span-1 p-1 border-l border-black">&nbsp;</div>
              <div class="col-span-1 p-1 border-l border-black">&nbsp;</div>
              <div class="col-span-2 p-1 border-l border-black">&nbsp;</div>
              <div class="col-span-1 p-1 border-l border-black">&nbsp;</div>
              <div class="col-span-1 p-1 border-l border-black">&nbsp;</div>
              <div class="col-span-1 p-1 border-l border-black">&nbsp;</div>
              <div class="col-span-1 p-1 border-l border-black">&nbsp;</div>
              <div class="col-span-1 p-1 border-l border-black">&nbsp;</div>
              <div class="col-span-1 p-1 border-l border-black">&nbsp;</div>
              <div class="col-span-1 p-1 border-l border-black">&nbsp;</div>
              <div class="col-span-1 p-1">&nbsp;</div>
            </div>

            <!-- Total Row -->
            <div class="grid grid-cols-12 border-b border-black font-bold">
              <div class="col-span-7 p-1 text-left border-l border-black">جمع کل</div>
              <div class="col-span-1 p-1 border-l border-black text-right">{{ formatCurrency(summary.totalAmount) }}</div>
              <div class="col-span-1 p-1 border-l border-black">&nbsp;</div>
              <div class="col-span-1 p-1 border-l border-black text-right">{{ formatCurrency(summary.totalAmount) }}</div>
              <div class="col-span-1 p-1 border-l border-black text-right">{{ formatCurrency(summary.totalTax) }}</div>
              <div class="col-span-1 p-1 text-right">{{ formatCurrency(summary.grandTotal) }}</div>
            </div>
            <div class="grid grid-cols-12">
              <!-- Signature and Total Amount -->
              <div class="grid grid-cols-12 col-span-6 border-l border-black">
                <div class="col-span-6 flex flex-col p-2 border-l border-black">
                  <div class="font-bold text-right mb-2">مهر و امضاء خریدار</div>
                  <div class="flex-grow min-h-[60px]"></div>
                </div>
                <div class="col-span-6 flex flex-col p-2">
                  <div class="font-bold text-right mb-2">مهر و امضاء فروشنده</div>
                  <div class="flex-grow min-h-[60px]"></div>
                </div>
              </div>

              <div class="grid grid-cols-12 col-span-6">
                <div class="col-span-12 p-2 font-bold text-right border-b border-black">
                  مبلغ قابل پرداخت (به عدد): {{ formatCurrency(summary.grandTotal) }} ریال
                </div>
                <div class="col-span-12 p-2 font-bold text-right">
                  مبلغ قابل پرداخت (به حروف): {{ summary.grandTotalInWords }} ریال
                </div>
              </div>
            </div>
          </div>
        </section>
        <div class="p-8 min-h-screen flex flex-col items-center">
          <button @click="printTable" class="mt-6 px-6 py-3 bg-blue-600 text-white font-bold rounded-lg shadow-md hover:bg-blue-700 transition duration-300">
            چاپ فاکتور (PDF)
          </button>
        </div>
      </section>
    </teleport>
  </div>
</template>

<style>
/* Optional: Add custom styles if Tailwind doesn't cover everything,
   but try to stick to Tailwind classes as much as possible. */
body {
  font-family: 'Inter', sans-serif; /* Using Inter font as per instructions */
}
</style>


