<template>
  <div>
    <teleport to="body">
      <section class="fixed inset-0 bg-gray-50 dark:bg-gray-900 z-50 overflow-y-auto">
        <section id="SalesInvoiceDiv"  class="bg-white p-8 min-h-screen flex flex-col items-center">
        
  <div class="havaleh-form">
    <h2>حواله خروج از انبار</h2>
    <div class="form-header">
      <div class="form-group">
        <label>تاریخ ارسال:</label>
        <input type="text" v-model="formData.date" />
      </div>
      <div class="form-group">
        <label>زمان ارسال:</label>
        <input type="text" v-model="formData.time" readonly />
      </div>
      <div class="form-group">
        <label>شماره سریال:</label>
        <input type="text" v-model="formData.serial" />
      </div>
    </div>

    <!-- Items Table -->
    <div class="items-table">

      <table>
        <thead>
          <tr>
            <th style="width: 5%">ردیف</th>
            <th style="width: 25%">نام کالا و مشخصات کالا</th>
            <th style="width: 7%">گرماژ</th>
            <th style="width: 7%">عرض کاغذ</th>
            <th style="width: 20%">نام خریدار</th>
            <th style="width: 10%">مقدار / تعداد</th>
            <th style="width: 15%">وزن کالا</th>
            <th style="width: 11%">عملیات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in formData.items" :key="index">
            <td>{{ index + 1 }}</td>
            <td>
              <div class="input-with-dropdown">
                <input type="text" v-model="item.name" placeholder="نام کالا را وارد کنید" class="product-input" />
              </div>
            </td>
            <td>
              <div class="input-with-dropdown">
                <input type="text" v-model="item.net_weight" placeholder="انتخاب گرماژ" class="net-weight-input" />
              </div>
            </td>
            <td>
              <input type="text" v-model="item.width" readonly placeholder="عرض کاغذ" />
            </td>
            <td>
              <input type="text" v-model="item.supplier_name" readonly placeholder="نام خریدار" />
            </td>
            <td>
              <input type="number" v-model="item.quantity" placeholder="تعداد" />
            </td>
            <td>
              <input type="number" v-model="item.weight" placeholder="وزن" />
            </td>
            <td>
              <button @click="removeItem(index)" class="remove-btn">حذف</button>
            </td>
          </tr>
          <tr v-if="formData.items.length === 0">
            <td>1</td>
            <td><input type="text" placeholder="نام کالا را وارد کنید" class="product-input" disabled /></td>
            <td><input type="text" placeholder="انتخاب گرماژ" class="net-weight-input" disabled /></td>
            <td><input type="text" placeholder="عرض کاغذ" disabled /></td>
            <td><input type="text" placeholder="نام خریدار" disabled /></td>
            <td><input type="number" placeholder="تعداد" disabled /></td>
            <td><input type="number" placeholder="وزن" disabled /></td>
            <td><button disabled class="remove-btn">حذف</button></td>
          </tr>
          <tr class="total-row-font">
            <td colspan="2">شماره پلاک: <span class="plate-number">{{ selectedProduct?.license_number ?
              formatPlateNumber(selectedProduct.license_number) : '' }}</span></td>
            <td colspan="3">نام راننده: {{ formData.name }}</td>
            <td>جمع: </td>
            <td>{{ calculateTotalWeight() }}</td>
          </tr>
        </tbody>
      </table>
      <div class="table-actions">
        <div class="left-actions">
          <button @click="showProductsList" class="action-btn view-btn">دریافت لیست محصولات</button>
        </div>
        <div class="right-actions">
          <button @click="returnToSalesOrder" class="action-btn return-btn">بازگشت به فاکتور فروش</button>
        </div>
      </div>
    </div>

    <div class="form-footer">
      <div class="form-group">
        <label>نام راننده:</label>
        <input type="text" v-model="formData.name" />
      </div>
      <div class="total-weight">
        <strong>جمع</strong> {{ calculateTotalWeight() }}
      </div>
      <button @click="submitForm" class="generate-btn">پیش نمایش</button>
    </div>

    <!-- Products List Modal -->
    <div v-if="showProductsModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>لیست محصولات</h2>
          <button class="close-button" @click="closeProductsModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="status-guide">وضعیت تمامی داده‌ها <strong>تحویل داده شده</strong> است.</div>
          <table class="modal-table">
            <thead>
              <tr>
                <th @click="sortModalProducts('grade')" class="sortable">
                  نام محصول
                  <span v-if="modalSortKey === 'grade'" class="sort-icon">
                    {{ modalSortOrder === 'asc' ? '↑' : '↓' }}
                  </span>
                </th>
                <th @click="sortModalProducts('gsm')" class="sortable">
                  گرماژ
                  <span v-if="modalSortKey === 'gsm'" class="sort-icon">
                    {{ modalSortOrder === 'asc' ? '↑' : '↓' }}
                  </span>
                </th>
                <th @click="sortModalProducts('width')" class="sortable">
                  عرض
                  <span v-if="modalSortKey === 'width'" class="sort-icon">
                    {{ modalSortOrder === 'asc' ? '↑' : '↓' }}
                  </span>
                </th>
                <th @click="sortModalProducts('customer_name')" class="sortable">
                  نام مشتری
                  <span v-if="modalSortKey === 'customer_name'" class="sort-icon">
                    {{ modalSortOrder === 'asc' ? '↑' : '↓' }}
                  </span>
                </th>
                <th @click="sortModalProducts('reel_count')" class="sortable">
                  تعداد رول
                  <span v-if="modalSortKey === 'reel_count'" class="sort-icon">
                    {{ modalSortOrder === 'asc' ? '↑' : '↓' }}
                  </span>
                </th>
                <th @click="sortModalProducts('net_weight')" class="sortable">
                  وزن کالا
                  <span v-if="modalSortKey === 'net_weight'" class="sort-icon">
                    {{ modalSortOrder === 'asc' ? '↑' : '↓' }}
                  </span>
                </th>
                <th @click="sortModalProducts('date')" class="sortable">
                  تاریخ
                  <span v-if="modalSortKey === 'date'" class="sort-icon">
                    {{ modalSortOrder === 'asc' ? '↑' : '↓' }}
                  </span>
                </th>
                <th @click="sortModalProducts('date')" class="sortable">
                  ساعت
                  <span v-if="modalSortKey === 'date'" class="sort-icon">
                    {{ modalSortOrder === 'asc' ? '↑' : '↓' }}
                  </span>
                </th>
                <th>{{ translateColumn('license_number') }}</th>
                <th>{{ translateColumn('list_of_reels') }}</th>
                <th>شماره فاکتور</th>
                <th>{{ translateColumn('actions') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="product in sortedModalProducts" :key="product.license_number">
                <td>{{ translateGrade(product.grade) }}</td>
                <td>{{ product.gsm }}</td>
                <td>{{ product.width }}</td>
                <td>{{ product.customer_name }}</td>
                <td>{{ product.reel_count }}</td>
                <td>{{ product.net_weight }}</td>
                <td>{{ formatTime(product.date).date }}</td>
                <td>{{ formatTime(product.date).time }}</td>
                <td>{{ product.license_number }}</td>
                <td>{{ product.list_of_reels }}</td>
                <td>{{ product.invoice_number }}</td>
                <td>
                  <button @click="selectProduct(product)" class="select-button">{{ translateColumn('select') }}</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- PDF Preview -->
    <div ref="pdfPreview" v-if="showData" class="pdf-preview">
      <div class="invoice-container">
        <div v-for="i in 3" :key="i" class="copy">
          <!-- Header Row -->
          <div class="header-row">
            <div class="company-name">شرکت صنایع تولیدی کاغذ و مقوای همایون</div>
            <div class="invoice-title">حواله خروج از انبار</div>
            <div class="fact-info fact-info-box">
              شماره حواله: {{ formData.serial || '-' }}<br>
              تاریخ ارسال: {{ formData.date || '-' }}<br>
              زمان ارسال: {{ formData.time || '-' }}
            </div>
            <div class="table-header">
              <img src="@/assets/images/homayoun-logo-new.png" alt="Homayoun Logo" class="table-logo" />
            </div>
          </div>

          <!-- Items Table -->
          <table class="details-table">
            <thead>
              <tr>
                <th style="width: 5%">ردیف</th>
                <th style="width: 25%">نام کالا و مشخصات کالا</th>
                <th style="width: 7%">گرماژ</th>
                <th style="width: 9%">عرض کاغذ</th>
                <th style="width: 20%">نام خریدار</th>
                <th style="width: 10%">مقدار / تعداد</th>
                <th style="width: 13%">وزن کالا</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in formData.items" :key="index">
                <td>{{ index + 1 }}</td>
                <td>{{ item.name }}</td>
                <td>{{ item.net_weight }}</td>
                <td>{{ item.width }}</td>
                <td>{{ item.supplier_name }}</td>
                <td>{{ item.quantity }}</td>
                <td>{{ item.weight }}</td>
              </tr>
            </tbody>
            <tfoot>
              <tr class="total-row">
                <td colspan="2">شماره پلاک: <span class="plate-number">{{
                  selectedProduct?.license_number ?
                    formatPlateNumber(selectedProduct.license_number) : '' }}</span></td>
                <td colspan="3">نام راننده: {{ formData.name }}</td>
                <td>جمع</td>
                <td>{{ calculateTotalWeight() }}</td>
              </tr>
            </tfoot>
          </table>

          <!-- Footer Section -->
          <table class="footer-table standard-bordered-table">
          <tbody>
            <tr>
              <td class="footer-signs">
                <div class="signs-row">
                  <div class="sign-box">حسابداری</div>
                  <div class="sign-box">انبارداری</div>
                  <div class="sign-box">مدیر فروش</div>
                  <div class="sign-box">مدیریت کارخانه</div>
                  <div class="sign-box">تحویل گیرنده</div>
                </div>
              </td>
            </tr>
          </tbody>
          </table>
          <div class="confirmation-text">
            بار صحیح و سالم تحویل اینجانب <span style="display:inline-block; width: 200px;"></span> گردید.
          </div>
          <hr class="header-line" v-if="i !== 3" />
          <div class="copy-number"></div>
        </div>
      </div>
    </div>
    <button type="button" @click="printPreview" v-if="showData" class="generate-btn">دریافت PDF</button>
  </div>
  
        </section>
      </section>
    </teleport>
  </div>
</template>

<script>
// import html2pdf from 'html2pdf.js';
import jalaali from 'jalaali-js';
import Lic_numer from "@/components/lic_numer.vue";
import { LicenseNumberParser } from "@/components/lic_num_split";
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8000';

export default {
  name: 'havaleh',
  components: {
    Lic_numer
  },
  data() {
    return {
      persianLetters: ['الف', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن', 'و', 'ه', 'ی'],
      products: [],
      showProductsModal: false,
      modalSortKey: 'date',
      modalSortOrder: 'desc',
      statusTranslations: {
        'In-stock': 'موجود در انبار',
        'Out-of-stock': 'ناموجود',
        'Pending': 'در انتظار',
        'Shipped': 'ارسال شده',
        'Delivered': 'تحویل داده شده',
        'Cancelled': 'لغو شده',
        'In Progress': 'در حال انجام',
        'Completed': 'تکمیل شده',
        'Rejected': 'رد شده',
        'Approved': 'تایید شده',
        'Processing': 'در حال پردازش',
        'Ready': 'آماده',
        'On Hold': 'در انتظار',
        'Active': 'فعال',
        'Inactive': 'غیرفعال'
      },
      gradeTranslations: {
        'Testliner HOMAYOUN': 'کاغذ تست لاینر',
        'Testliner': 'کاغذ تست لاینر',
        'Flutting HOMAYOUN': 'کاغذ فلوت',
        'Flutting': 'کاغذ فلوت',
        'تست لاینر همایون': 'کاغذ تست لاینر همایون',
        'تست لاینر': 'کاغذ تست لاینر',
        'فلوت همایون': 'کاغذ فلوت همایون',
        'فلوت': 'کاغذ فلوت',
      },
      columnTranslations: {
        'status': 'وضعیت',
        'license_number': 'شماره پلاک',
        'list_of_reels': 'لیست رول‌ها',
        'actions': 'عملیات',
        'select': 'انتخاب'
      },
      formData: {
        date: this.getCurrentDate(),
        time: this.getCurrentTime(),
        serial: '',
        items: [],
        driver_name: '',
        plate_number: ''
      },
      selectedProduct: null,
      showData: false,
      showPdfButton: false,
    }
  },
  computed: {
    sortedModalProducts() {
      if (!this.products) return [];

      return [...this.products].sort((a, b) => {
        const key = this.modalSortKey;
        const isAsc = this.modalSortOrder === 'asc';

        // تبدیل اعداد فارسی به انگلیسی
        const toEnglish = (str) => {
          if (!str) return '';
          return String(str).replace(/[۰-۹]/g, d => '۰۱۲۳۴۵۶۷۸۹'.indexOf(d));
        };

        // برای فیلدهای عددی (گرماژ، عرض، تعداد رول، وزن)
        if (['gsm', 'width', 'reel_count', 'net_weight'].includes(key)) {
          const aNum = parseFloat(toEnglish(a[key])) || 0;
          const bNum = parseFloat(toEnglish(b[key])) || 0;
          return isAsc ? aNum - bNum : bNum - aNum;
        }

        // برای تاریخ و زمان
        if (key === 'date') {
          const aDate = a.date ? new Date(a.date) : new Date(0);
          const bDate = b.date ? new Date(b.date) : new Date(0);
          return isAsc ? aDate - bDate : bDate - aDate;
        }

        // برای نام محصول
        if (key === 'grade') {
          const aText = toEnglish(this.translateGrade(a[key] || ''));
          const bText = toEnglish(this.translateGrade(b[key] || ''));
          return isAsc ?
            aText.localeCompare(bText, 'fa') :
            bText.localeCompare(aText, 'fa');
        }

        // برای سایر فیلدهای متنی
        const aText = toEnglish(a[key] || '');
        const bText = toEnglish(b[key] || '');
        return isAsc ?
          aText.localeCompare(bText, 'fa') :
          bText.localeCompare(aText, 'fa');
      });
    }
  },
  created() {
    // تنظیم تایتل مرورگر در ابتدای ایجاد کامپوننت
    if (this.formData.serial && this.formData.serial.trim()) {
      document.title = `Havaleh - ${this.formData.serial.trim()}`;
    } else {
      document.title = 'Havaleh';
    }

    this.formData.date = this.getCurrentDate();
    this.formData.time = this.getCurrentTime();
    this.fetchProducts();

    // خواندن داده‌های فاکتور فروش از localStorage
    const lastSaleData = localStorage.getItem('lastSaleData');
    if (lastSaleData) {
      try {
        const saleData = JSON.parse(lastSaleData);

        // Populate form data
        this.formData.serial = saleData.serial || '';
        // تنظیم تایتل مرورگر بر اساس شماره سریال
        if (this.formData.serial && this.formData.serial.trim()) {
          document.title = `Havaleh - ${this.formData.serial.trim()}`;
        }

        this.formData.date = saleData.date || this.getCurrentDate();
        this.formData.time = this.getCurrentTime();

        // Set license plate data
        if (saleData.license_number) {
          this.selectedProduct = {
            license_number: saleData.license_number,
            plate_first: saleData.plate_first,
            plate_letter: saleData.plate_letter,
            plate_second: saleData.plate_second,
            plate_year: saleData.plate_year
          };
        }

        // Clear existing items
        this.formData.items = [];

        // Add items from sales order
        if (saleData.items && saleData.items.length > 0) {
          saleData.items.forEach(item => {
            // Extract gsm and width from description
            const gsmMatch = item.description.match(/گرماژ\s*(\d+)/);
            const widthMatch = item.description.match(/عرض\s*(\d+)/);

            const gsm = gsmMatch ? gsmMatch[1] : '';
            const width = widthMatch ? widthMatch[1] : '';

            this.formData.items.push({
              name: item.name,
              net_weight: gsm, // گرماژ
              width: width, // عرض
              supplier_name: saleData.buyer_name || '',
              quantity: item.reelCount || item.quantity || 0,  // استفاده از تعداد رول‌ها
              weight: item.weight || item.total || 0 // استفاده از weight یا total
            });
          });
        }

        // Clear localStorage after reading
        localStorage.removeItem('lastSaleData');
      } catch (error) {
        console.error('Error parsing sales order data:', error);
      }
    }

    // خواندن داده‌های حواله از localStorage (اگر از فاکتور فروش برگشته باشد)
    const lastHavalehData = localStorage.getItem('lastHavalehData');
    if (lastHavalehData) {
      try {
        const havalehData = JSON.parse(lastHavalehData);

        // پر کردن فرم با داده‌های ذخیره شده
        this.formData.serial = havalehData.serial || '';
        // تنظیم تایتل مرورگر بر اساس شماره سریال
        if (this.formData.serial && this.formData.serial.trim()) {
          document.title = `Havaleh - ${this.formData.serial.trim()}`;
        }

        this.formData.date = havalehData.date || this.getCurrentDate();
        this.formData.time = havalehData.time || this.getCurrentTime();

        // تنظیم داده‌های پلاک
        if (havalehData.license_number) {
          this.selectedProduct = {
            license_number: havalehData.license_number
          };
        }

        // پاک کردن آیتم‌های موجود
        this.formData.items = [];

        // اضافه کردن آیتم‌ها از داده‌های ذخیره شده
        if (havalehData.items && havalehData.items.length > 0) {
          havalehData.items.forEach(item => {
            // استخراج گرماژ و عرض از توضیحات
            const gsmMatch = item.description.match(/گرماژ\s*(\d+)/);
            const widthMatch = item.description.match(/عرض\s*(\d+)/);

            const gsm = gsmMatch ? gsmMatch[1] : '';
            const width = widthMatch ? widthMatch[1] : '';

            this.formData.items.push({
              name: item.name,
              net_weight: gsm,
              width: width,
              supplier_name: havalehData.buyer_name || '',
              quantity: item.reelCount || item.quantity || 0,  // استفاده از تعداد رول‌ها
              weight: item.weight || item.total || 0 // استفاده از weight یا total
            });
          });
        }

        // پاک کردن localStorage بعد از خواندن
        localStorage.removeItem('lastHavalehData');
      } catch (error) {
        console.error('Error parsing havaleh data:', error);
      }
    }
  },
  mounted() {
    // تنظیم تایتل مرورگر در ابتدای ورود به صفحه
    if (this.formData.serial && this.formData.serial.trim()) {
      document.title = `Havaleh - ${this.formData.serial.trim()}`;
    } else {
      document.title = 'Havaleh';
    }

    document.addEventListener('click', this.handleClickOutside);
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleClickOutside);
  },
  watch: {
    'formData.serial': {
      handler(newValue) {
        if (newValue && newValue.trim()) {
          document.title = `Havaleh - ${newValue.trim()}`;
        } else {
          document.title = 'Havaleh';
        }
      },
      immediate: true
    }
  },
  methods: {
    getCurrentDate() {
      const today = new Date();
      const jDate = jalaali.toJalaali(today);
      return `${jDate.jy}/${String(jDate.jm).padStart(2, '0')}/${String(jDate.jd).padStart(2, '0')}`;
    },
    getCurrentTime() {
      const today = new Date();
      const iranOffset = 4.5 * 60; // Iran is UTC+3:30
      const localOffset = today.getTimezoneOffset();
      const totalOffset = (iranOffset + localOffset) * 60 * 1000;
      const iranTime = new Date(today.getTime() + totalOffset);
      return `${String(iranTime.getHours()).padStart(2, '0')}:${String(iranTime.getMinutes()).padStart(2, '0')}`;
    },
    addItem() {
      this.formData.items.push({
        name: '',
        net_weight: '',
        width: '',
        supplier_name: '',
        quantity: '',
        weight: '',
        unit: 'کیلو'
      });
    },
    removeItem(index) {
      this.formData.items.splice(index, 1);
    },
    calculateTotalWeight() {
      return this.formData.items.reduce((total, item) => {
        return total + (parseFloat(item.weight) || 0);
      }, 0).toLocaleString();
    },
    calculateTotalQuantity() {
      return this.formData.items.reduce((total, item) => {
        return total + (parseFloat(item.quantity) || 0);
      }, 0).toLocaleString();
    },
    parsePlateNumber(plateNumber) {
      const parsed = LicenseNumberParser(plateNumber);
      if (parsed) {
        this.formData.plate = parsed;
      }
    },
    printPreview() {
      // Convert Persian numbers to English for the filename
      const invoiceNumber = this.formData.serial ? this.convertToEnglishNumbers(this.formData.serial) : 'NoNumber';
      const fileName = `Havaleh-${invoiceNumber}.pdf`;

      // Add a hidden input to set the filename
      const input = document.createElement('input');
      input.type = 'hidden';
      input.name = 'filename';
      input.value = fileName;
      document.body.appendChild(input);

      // Create a style element for print orientation
      const style = document.createElement('style');
      style.id = 'print-style';
      style.innerHTML = `
        @page {
          size: A4 portrait !important;
          margin: 0 !important;
        }
        @media print {
          body {
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
          }
        }
      `;
      document.head.appendChild(style);

      // Print the document
      const printContent = document.querySelector('.pdf-preview');
      const originalContent = document.body.innerHTML;
      document.body.innerHTML = printContent.outerHTML;
      window.print();
      document.body.innerHTML = originalContent;

      // Remove the hidden input and style
      document.body.removeChild(input);
      const addedStyle = document.getElementById('print-style');
      if (addedStyle) {
        addedStyle.remove();
      }

      // Hide the PDF button after printing
      this.showPdfButton = false;
    },

    async generatePDF() {
      const element = this.$refs.pdfPreview;
      const opt = {
        margin: [10, 10, 10, 10],
        filename: `Havaleh${this.formData.serial || 'NoNumber'}.pdf`,
        image: { type: 'jpeg', quality: 1 },
        html2canvas: {
          scale: 2,
          useCORS: true,
          letterRendering: true,
          scrollY: 0,
          scrollX: 0,
          backgroundColor: '#ffffff',
          logging: true,
          allowTaint: true,
          foreignObjectRendering: true,
          removeContainer: true,
          windowWidth: element.scrollWidth,
          windowHeight: element.scrollHeight
        },
        jsPDF: {
          unit: 'mm',
          format: 'a4',
          orientation: 'portrait',
          putOnlyUsedFonts: true,
          floatPrecision: 16,
          compress: true,
          hotfixes: ['px_scaling'],
          precision: 16
        },
        pagebreak: {
          mode: 'avoid-all',
          before: '.page-break-before',
          after: '.page-break-after'
        }
      };

      // Add a class to the element to ensure proper styling
      element.classList.add('pdf-export');

      // Wait for fonts to load
      await document.fonts.ready;

      // Generate PDF
      await html2pdf().set(opt).from(element).save();

      // Remove the class after export
      element.classList.remove('pdf-export');
    },
    async fetchProducts() {
      try {
        const response = await axios.get('/myapp/api/products/list');
        console.log('API Response:', response.data);
        if (response.data && response.data.status === 'success' && response.data.data && response.data.data.products) {
          this.products = response.data.data.products;
          console.log('Products loaded:', this.products);
        } else {
          console.error('Invalid response format:', response.data);
          this.products = [];
        }
      } catch (error) {
        console.error('Error fetching products:', error.response?.data || error.message);
        this.products = [];
      }
    },
    convertToEnglishNumbers(text) {
      if (!text) return '';
      return text.replace(/[۰-۹]/g, d => '۰۱۲۳۴۵۶۷۸۹'.indexOf(d));
    },
    selectProduct(product) {
      this.selectedProduct = product;
      if (product.license_number) {
        product.license_number = this.convertToEnglishNumbers(product.license_number);
      }
      this.formData.serial = product.invoice_number || '';

      // شمارش تعداد رول‌ها از list_of_reels
      const reelCount = this.countReelsFromList(product.list_of_reels);

      this.formData.items.push({
        name: this.translateGrade(product.grade) || '',  // استفاده از ترجمه گرید
        net_weight: product.gsm || '',
        width: product.width || '',
        supplier_name: product.customer_name || '',
        quantity: reelCount || product.reel_count || '',  // استفاده از تعداد رول‌های شمرده شده
        weight: product.net_weight || '',  // استفاده از net_weight به عنوان وزن کالا
        license_number: product.license_number ? this.convertToEnglishNumbers(product.license_number) : '',
        list_of_reels: product.list_of_reels || ''
      });
      this.closeProductsModal();
    },
    closeProductsModal() {
      this.showProductsModal = false;
    },
    sortModalProducts(key) {
      // اگر روی همان ستون کلیک شد، ترتیب را تغییر بده
      if (this.modalSortKey === key) {
        this.modalSortOrder = this.modalSortOrder === 'asc' ? 'desc' : 'asc';
      } else {
        // اگر ستون جدید انتخاب شد، آن را به عنوان کلید مرتب‌سازی تنظیم کن
        this.modalSortKey = key;
        // برای ستون تاریخ، پیش‌فرض نزولی باشد
        this.modalSortOrder = key === 'date' ? 'desc' : 'asc';
      }
    },
    translateStatus(status) {
      return this.statusTranslations[status] || status;
    },
    translateColumn(column) {
      return this.columnTranslations[column] || column;
    },
    translateGrade(grade) {
      // Remove "HOMAYOUN" from the grade if it exists
      const cleanGrade = grade.replace(/\s*HOMAYOUN\s*/i, '');
      return this.gradeTranslations[cleanGrade] || cleanGrade;
    },
    handleClickOutside(event) {
      const productInputs = document.querySelectorAll('.product-input');
      const netWeightInputs = document.querySelectorAll('.net-weight-input');
      const dropdowns = document.querySelectorAll('.dropdown-list');

      let clickedInsideProduct = false;
      let clickedInsideNetWeight = false;
      let clickedInsideDropdown = false;

      productInputs.forEach(input => {
        if (input.contains(event.target)) {
          clickedInsideProduct = true;
        }
      });

      netWeightInputs.forEach(input => {
        if (input.contains(event.target)) {
          clickedInsideNetWeight = true;
        }
      });

      dropdowns.forEach(dropdown => {
        if (dropdown.contains(event.target)) {
          clickedInsideDropdown = true;
        }
      });

      if (!clickedInsideProduct && !clickedInsideNetWeight && !clickedInsideDropdown) {
        this.showProductDropdown = false;
        this.showNetWeightDropdown = false;
      }
    },
    async showProductsList() {
      try {
        const response = await axios.get('/myapp/api/products/list');
        console.log('API Response:', response.data);
        if (response.data && response.data.status === 'success' && response.data.data && response.data.data.products) {
          this.products = response.data.data.products;
          this.showProductsModal = true;
        } else {
          console.error('Invalid response format:', response.data);
          alert('خطا در دریافت اطلاعات محصولات: فرمت پاسخ نامعتبر است');
        }
      } catch (error) {
        console.error('Error fetching products:', error);
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          console.error('Error response:', error.response.data);
          alert(`خطا در دریافت اطلاعات محصولات: ${error.response.data.message || 'خطای سرور'}`);
        } else if (error.request) {
          // The request was made but no response was received
          console.error('No response received:', error.request);
          alert('خطا در دریافت اطلاعات محصولات: سرور پاسخ نمی‌دهد');
        } else {
          // Something happened in setting up the request that triggered an Error
          console.error('Error setting up request:', error.message);
          alert('خطا در دریافت اطلاعات محصولات: خطای شبکه');
        }
      }
    },
    submitForm() {
      this.formData.date = this.getCurrentDate();
      this.formData.time = this.getCurrentTime();
      this.showData = true;
      this.showPdfButton = true;
    },
    formatPlateNumber(plateNumber) {
      if (!plateNumber) return '';

      const numbers = plateNumber.replace(/[^0-9]/g, '');
      const letters = plateNumber.match(/[آ-ی]/g) || [];
      let letter = letters.length > 0 ? letters[0] : '';

      if (letter === 'ا') {
        letter = 'الف';
      }

      const lastPart = numbers.slice(-2);       // مثلاً 68
      const middlePart = numbers.slice(-5, -2); // مثلاً 515
      const firstPart = numbers.slice(0, 2);    // مثلاً 35

      return `${lastPart} - ${middlePart} ${letter} ${firstPart}`;
    },
    returnToSalesOrder() {
      // ذخیره داده‌های فعلی حواله در localStorage
      const havalehData = {
        serial: this.formData.serial,
        date: this.formData.date,
        time: this.formData.time,
        items: this.formData.items.map(item => ({
          name: item.name,
          description: `گرماژ ${item.net_weight} عرض ${item.width}`,
          quantity: item.quantity,  // تعداد رول‌ها
          total: item.weight, // ذخیره وزن در فیلد total
          weight: item.weight, // اضافه کردن فیلد weight
          reelCount: item.quantity  // اضافه کردن فیلد تعداد رول‌ها
        })),
        buyer_name: this.formData.items[0]?.supplier_name || '',
        license_number: this.selectedProduct?.license_number || ''
      };

      localStorage.setItem('lastHavalehData', JSON.stringify(havalehData));

      // هدایت به صفحه فاکتور فروش
      this.$router.push('/myapp/invoice/sales_order');
    },
    formatTime(timestamp) {
      if (!timestamp) return { date: '', time: '' };

      // تبدیل تاریخ به فرمت شمسی
      const date = new Date(timestamp);
      const jDate = jalaali.toJalaali(date);

      // فرمت‌بندی تاریخ و زمان
      const year = jDate.jy;
      const month = String(jDate.jm).padStart(2, '0');
      const day = String(jDate.jd).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');

      return {
        date: `${year}/${month}/${day}`,
        time: `${hours}:${minutes}`
      };
    },
    countReelsFromList(listOfReels) {
      if (!listOfReels || listOfReels.trim() === '') {
        return 0;
      }
      // شمارش تعداد رول‌ها بر اساس کاما
      const reels = listOfReels.split(',').filter(reel => reel.trim() !== '');
      return reels.length;
    },
  }
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

.havaleh-form {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); */
  direction: rtl;
  font-family: 'BNazanin', Arial, sans-serif !important;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
  font-size: 50px;
}

.form-header {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  font-size: 25px;
}

.form-group {
  flex: 1;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.items-table {
  margin: 20px 0;
  overflow-x: auto;
  font-size: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

th,
td {
  padding: 5px;
  text-align: center;
}

th {
  background-color: #f5f5f5;
  font-weight: bold;
  text-align: center;
}

input[type="text"],
input[type="number"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: center;
  font-size: 20px;
}

.remove-btn {
  background-color: #ff4444;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.add-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;
}

.form-footer {
  margin-top: 20px;
}

.total-weight {
  margin: 20px 0;
  font-size: 1.2em;
  font-weight: bold;
}

.generate-btn {
  background-color: #2196F3;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.1em;
  margin-top: 15px;
}

button:hover {
  opacity: 0.9;
}

textarea {
  width: 100%;
  min-height: 100px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
}


#pdf-template {
  font-family: 'BNazanin', Arial, sans-serif !important;
  direction: rtl;
  font-size: 12pt;
  background: white;
  width: 1120px;
  max-width: 100vw;
  margin-left: auto;
  margin-right: auto;
  margin-top: 30px;
  background: #fff;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  font-size: 0.95em;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#pdf-template .header-row {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  margin-top: 10px;
  text-align: center;
}

#pdf-template .company-name {
  font-size: 1.8em;
  font-weight: bold;
  text-align: center;
  margin-bottom: 0px;
  width: 100%;
  color: #000;
}

#pdf-template .invoice-title {
  text-align: center;
  font-size: 1.2em;
  margin-top: 0px;
  margin-bottom: 5px;
  width: 100%;
}

#pdf-template .fact-info-box {
  position: absolute;
  top: 0px;
  right: 10px;
  border-radius: 8px;
  background: #fff;
  font-size: 1.1em;
  text-align: right;
  direction: rtl;
  display: inline-block;
  min-width: 160px;
  max-width: 200px;
  line-height: 1.45;
}

#pdf-template .details-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 2px;
  margin-bottom: 0;
}

#pdf-template .details-table th,
#pdf-template .details-table td {
  border: 1.5px solid #444;
  padding: 10px;
  text-align: center;
  vertical-align: middle;
}

#pdf-template .details-table th {
  background: #e9ecef;
  font-weight: bold;
  padding: 4px 3px;
  text-align: center;
  vertical-align: middle;
}

#pdf-template .details-table .total-row td {
  font-weight: bold;
  background: #f5f5f5;
  border-top: 2.5px solid #444;
  font-size: 1em;
  padding: 4px 3px;
  text-align: center;
  vertical-align: middle;
}

#pdf-template .footer-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0;
  margin-bottom: 0;
  margin-right: auto;
  margin-left: 0;
  border: none;
}

#pdf-template .footer-table td {
  vertical-align: top;
  padding: 10px 0px 0px 0px;
  border: none;
}

#pdf-template .footer-signs {
  width: 100%;
}

#pdf-template .footer-signs .signs-row {
  display: flex;
  flex-direction: row;
  gap: 15px;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0;
  padding: 4px 0px;
}

#pdf-template .footer-signs .sign-box {
  border-top: none;
  width: 120px;
  text-align: center;
  padding-top: 4px;
  font-size: 0.9em;
  margin-bottom: 0;
}

#pdf-template .confirmation-text {
  text-align: center;
  font-size: 1em;
  margin-top: 10px;
  padding: 4px;
  border: none;
}

#pdf-template .plate-number {
  font-size: 1.3em;
  font-weight: bold;
  letter-spacing: 1px;
  word-spacing: 2px;
  white-space: nowrap;
}

#pdf-template .header-line {
  border: none;
  border-top: 1px solid #000000;
  margin-right: 0px;
  margin-bottom: 10px;
  margin-left: 0px;
  padding-top: 2px;
}

.plate-input {
  display: none;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 95%;
  max-width: 1400px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.5em;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
  color: #666;
  padding: 5px;
}

.close-button:hover {
  color: #333;
}

.modal-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  font-size: 0.9em;
}

.modal-table th,
.modal-table td {
  padding: 8px;
  text-align: right;
  border-bottom: 1px solid #eee;
  white-space: nowrap;
}

.modal-table th {
  background-color: #f8f9fa;
  font-weight: bold;
  color: #333;
  position: sticky;
  top: 0;
  z-index: 1;
}

.modal-table td {
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.modal-table tr:hover {
  background-color: #f5f5f5;
}

.modal-table td:last-child {
  white-space: nowrap;
  min-width: 80px;
}

.select-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.select-button:hover {
  background-color: #45a049;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 16px;
  margin-bottom: 8px;
}

.btn-action {
  min-width: 140px;
  min-height: 48px;
  padding: 12px 24px;
  font-size: 1.1em;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  display: inline-block;
  box-sizing: border-box;
}

.view-btn {
  background-color: #607D8B;
  color: white;
}

.view-btn:hover {
  background-color: #546E7A;
}

.add-btn:hover {
  background-color: #45a049;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.return-btn {
  background-color: #FF9800;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
  transition: background-color 0.2s;
  white-space: nowrap;
  outline: none;
}

.return-btn:hover {
  background-color: #F57C00;
}

.return-btn:focus {
  outline: none;
  box-shadow: none;
}

.return-btn:active {
  outline: none;
  box-shadow: none;
}

/* Mobile Responsive Styles */
@media screen and (max-width: 768px) {
  .havaleh-form {
    margin: 10px;
    padding: 10px;
    width: auto;
    overflow-x: hidden;
    display: none;
  }

  .form-header {
    flex-direction: column;
    gap: 10px;
  }

  .form-group {
    width: 100%;
  }

  .form-group input {
    width: 100%;
    font-size: 16px;
    /* Prevent zoom on iOS */
  }

  .items-table {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  table {
    min-width: 800px;
    /* Ensure table doesn't break on mobile */
  }

  .form-footer {
    flex-direction: column;
  }

  .form-footer .form-group {
    width: 100%;
  }

  .total-weight {
    text-align: center;
    margin: 15px 0;
  }

  .generate-btn {
    width: 100%;
    margin: 10px 0;
  }

  /* PDF Template Mobile Styles */
  #pdf-template {
    width: 100%;
    padding: 5mm;
  }

  #pdf-template .header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  #pdf-template .logo-section {
    width: 100%;
    text-align: center;
    margin-bottom: 10px;
  }

  #pdf-template .company-info {
    margin: 10px 0;
  }

  #pdf-template .document-info {
    width: 100%;
    margin-top: 10px;
  }

  #pdf-template table {
    font-size: 8pt;
  }

  #pdf-template th,
  #pdf-template td {
    padding: 2mm;
  }

  #pdf-template .footer {
    flex-direction: column;
    gap: 10px;
  }

  #pdf-template .signature-line {
    width: 100%;
    margin-bottom: 10px;
  }

  .table-logo {
    width: 100px;
  }
}

/* iPhone Specific Styles */
@supports (-webkit-touch-callout: none) {

  .form-group input,
  .plate-input input,
  .plate-input select {
    font-size: 16px;
    /* Prevent zoom on iOS */
  }

  .items-table {
    -webkit-overflow-scrolling: touch;
  }

  .dropdown-list {
    max-height: 200px;
    -webkit-overflow-scrolling: touch;
  }
}

.product-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  cursor: text;
}

.product-input:focus {
  outline: none;
  border-color: #2196F3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
}

.net-weight-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  cursor: text;
}

.net-weight-input:focus {
  outline: none;
  border-color: #2196F3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
}

.net-weight-input option {
  padding: 8px;
  font-size: 14px;
}

.table-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
  width: 100%;
}

.left-actions,
.right-actions {
  display: flex;
  gap: 16px;
}

.action-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
  transition: background-color 0.2s;
  white-space: nowrap;
  outline: none;
  min-width: 160px;
  /* عرض یکسان برای هر دو دکمه */
  text-align: center;
}

.view-btn {
  background-color: #607D8B;
  color: white;
}

.view-btn:hover {
  background-color: #546E7A;
}

.return-btn {
  background-color: #FF9800;
  color: white;
}

.return-btn:hover {
  background-color: #F57C00;
}

.action-btn:focus,
.action-btn:active {
  outline: none;
  box-shadow: none;
}

/* حذف استایل‌های قبلی که دیگر استفاده نمی‌شوند */
.add-btn {
  display: none;
}

.sortable {
  cursor: pointer;
  user-select: none;
  position: relative;
}

.sortable:hover {
  background-color: #e9ecef;
}

.sort-icon {
  margin-right: 5px;
  font-size: 0.8em;
}

.modal-table th {
  white-space: nowrap;
  padding: 12px 8px;
}

.modal-table td {
  padding: 8px;
  vertical-align: middle;
}

.select-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
  transition: background-color 0.2s;
}

.select-button:hover {
  background-color: #45a049;
}

.info-row {
  background-color: #f8f9fa;
  font-weight: bold;
}

.info-row td {
  padding: 8px;
  text-align: right;
  border: 1px solid #ddd;
}

/* Add styles from salesorder.vue */
.pdf-preview {
  width: 1120px;
  max-width: 100vw;
  margin-left: auto;
  margin-right: auto;
  margin-top: 30px;
  background: #fff;
  padding: 12px;
  border-radius: 8px;
  /* box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); */
  font-size: 0.95em;
  font-family: 'BNazanin', Arial, sans-serif !important;
}

.invoice-container {
  width: 100%;
  margin: 0;
  padding: 0mm;
  background: #fff;
  box-sizing: border-box;
  position: relative;
  font-size: 0.95em;
  font-family: 'BNazanin', Arial, sans-serif !important;
}

.copy {
  width: 100%;
  margin-bottom: 0;
  padding-bottom: 0;
  transform-origin: top;
  transform: scale(0.95);
  font-family: 'BNazanin', Arial, sans-serif !important;
}

.copy-number {
  position: absolute;
  top: 10px;
  left: 10px;
  font-size: 1.2em;
  font-weight: bold;
  color: #666;
}

.header-row {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: 0px;
  margin-top: 0px;
  text-align: center;
}

.company-name {
  font-size: 1.5em;
  font-weight: bold;
  text-align: center;
  margin-bottom: 0px;
  width: 50%;
  color: #000;
  font-family: 'BNazanin', Arial, sans-serif !important;
}

.invoice-title {
  text-align: center;
  font-size: 1.8em;
  margin-top: 0px;
  margin-bottom: 5px;
  width: 30%;
  font-family: 'BNazanin', Arial, sans-serif !important;
}

.fact-info-box {
  position: absolute;
  top: 0px;
  right: 10px;
  border-radius: 8px;
  background: #fff;
  font-size: 1.3em;
  text-align: right;
  direction: rtl;
  display: inline-block;
  min-width: 160px;
  max-width: 200px;
  font-family: 'BNazanin', Arial, sans-serif !important;
  line-height: 1.45;
}

.details-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
  margin-bottom: 0;
  font-size: 16px;
  font-family: 'BNazanin', Arial, sans-serif !important;
}

.details-table th,
.details-table td {
  border: 1.5px solid #444;
  padding: 6px;
  text-align: center;
  vertical-align: middle;
  font-family: 'BNazanin', Arial, sans-serif !important;
}

.details-table .total-row td {
  font-weight: bold;
  background: #f5f5f5;
  border-top: 2.5px solid #444;
  font-size: 1em;
  padding: 4px 3px;
  text-align: center;
  vertical-align: middle;
}

.footer-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0;
  margin-bottom: 0;
  margin-right: auto;
  margin-left: 0;
  border: none;
  font-family: 'BNazanin', Arial, sans-serif !important;
}

.footer-signs {
  width: 100%;
}

.footer-signs .signs-row {
  display: flex;
  flex-direction: row;
  gap: 15px;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0;
  padding: 5px 0px;
}

.footer-signs .sign-box {
  border-top: none;
  width: 120px;
  text-align: center;
  padding-top: 4px;
  font-size: 1.3em;
  margin-bottom: 0;
  font-family: 'BNazanin', Arial, sans-serif !important;
}

.confirmation-text {
  text-align: center;
  font-size: 1.5em;
  margin-top: 8px;
  padding: 0px;
  border: none;
  font-family: 'BNazanin', Arial, sans-serif !important;
}

.header-line {
  border: none;
  border-top: 1px solid #000000;
  margin-top: 20px;
  margin-right: 0px;
  margin-bottom: 0px;
  margin-left: 0px;
  padding-top: 8px;
  display: none;
  /* Hide by default */
}

.header-line:not(:last-child) {
  display: block;
  /* Show only if not the last copy */
}

.total-row-font {

  font-family: 'BNazanin', Arial, sans-serif !important;
  background-color: #f5f5f5;
}

/* Add print-specific styles */
@media print {
  @page {
    size: A4 portrait;
    margin: 0;
  }

  .pdf-preview,
  .invoice-container,
  .copy,
  .company-name,
  .invoice-title,
  .fact-info-box,
  .details-table,
  .details-table th,
  .details-table td,
  .footer-table,
  .footer-signs .sign-box,
  .confirmation-text {
    font-family: 'BNazanin', Arial, sans-serif !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
}

.status-guide {
  background-color: #e3f2fd;
  color: #1565c0;
  padding: 10px 15px;
  border-radius: 4px;
  margin-bottom: 15px;
  text-align: center;
  font-size: 1.1em;
  border: 1px solid #bbdefb;
  font-weight: bold;
}

input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
  opacity: 0.7;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
  opacity: 0.7;
}

.table-header {
  position: absolute;
  left: 10px;
  z-index: 1;
}

.table-logo {
  width: 170px;
  height: auto;
  object-fit: contain;
}

@media screen and (max-width: 768px) {
  .table-header {
    left: 10px;
    top: 10px;
  }

  .table-logo {
    width: 80px;
  }
}
</style>