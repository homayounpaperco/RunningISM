<template>
  <div>
    <teleport to="body">
      <section class="fixed inset-0 bg-gray-50 dark:bg-gray-900 z-50 overflow-y-auto">
        <section id="SalesInvoiceDiv"  class="bg-white p-8 min-h-screen flex flex-col items-center">
        
  <div class="">
    <!-- Name Mismatch Warning -->
    <div v-if="nameMismatchWarning" class="name-warning">
      {{ nameMismatchWarning }}
    </div>
    <!-- Form section (unchanged) -->
    <form @submit.prevent="submitForm">
      <div>
        <h1 class="page-title">فاکتور فروش</h1>
      </div>
      <div class="form-row">
        <label>شماره فاکتور:</label>
        <input v-model="form.serial" required />
        <label>تاریخ امروز:</label>
        <input v-model="form.date" required />
        <label>تاریخ فروش:</label>
        <input v-model="form.sale_date" readonly />
      </div>
      <div style="display: flex; flex-direction: column; gap: 1rem; max-width: 100%; padding: 1rem;">
        <!-- سطر اول: نام خریدار (25%) و نشانی خریدار (75%) -->
        <div style="display: flex; flex-direction: row; gap: 1rem; width: 100%;">
          <div style="display: flex; flex-direction: column; flex: 25%;">
            <label style="margin-bottom: 0.5rem; font-weight: bold;">نام خریدار:</label>
            <input v-model="form.buyer_name" required inputmode="text"
              @input="form.buyer_name = $event.target.value.replace(/[^آ-ی\s]/g, '')"
              placeholder="فقط حروف فارسی وارد کنید"
              style="padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; width: 100%; box-sizing: border-box;" />
          </div>
          <div style="display: flex; flex-direction: column; flex: 75%;">
            <label style="margin-bottom: 0.5rem; font-weight: bold;">نشانی خریدار:</label>
            <input v-model="form.buyer_address" placeholder="محدودیتی ندارد"
              style="padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; width: 100%; box-sizing: border-box;" />
          </div>
        </div>

        <!-- سطر دوم: شماره اقتصادی، شماره ثبت و کد ملی (هر کدام 33%) -->
        <div style="display: flex; flex-direction: row; gap: 1rem; width: 100%;">
          <div style="display: flex; flex-direction: column; flex: 33.33%;">
            <label style="margin-bottom: 0.5rem; font-weight: bold;">شماره اقتصادی خریدار:</label>
            <input v-model="form.buyer_economic_code" inputmode="numeric"
              @input="form.buyer_economic_code = $event.target.value.replace(/\D/g, '')" placeholder="فقط عدد وارد کنید"
              style="padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; width: 100%; box-sizing: border-box;" />
          </div>
          <div style="display: flex; flex-direction: column; flex: 33.33%;">
            <label style="margin-bottom: 0.5rem; font-weight: bold;">شماره ثبت خریدار:</label>
            <input v-model="form.buyer_reg" inputmode="numeric"
              @input="form.buyer_reg = $event.target.value.replace(/\D/g, '')" placeholder="فقط عدد وارد کنید"
              style="padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; width: 100%; box-sizing: border-box;" />
          </div>
          <div style="display: flex; flex-direction: column; flex: 33.33%;">
            <label style="margin-bottom: 0.5rem; font-weight: bold;">کد ملی خریدار:</label>
            <input v-model="form.buyer_national_id" inputmode="numeric"
              @input="form.buyer_national_id = $event.target.value.replace(/\D/g, '')" placeholder="فقط عدد وارد کنید"
              style="padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; width: 100%; box-sizing: border-box;" />
          </div>
        </div>

        <!-- سطر سوم: کد پستی و تلفن (هر کدام 50%) -->
        <div style="display: flex; flex-direction: row; gap: 1rem; width: 100%;">
          <div style="display: flex; flex-direction: column; flex: 50%;">
            <label style="margin-bottom: 0.5rem; font-weight: bold;">کد پستی خریدار:</label>
            <input v-model="form.buyer_postcode" inputmode="numeric"
              @input="form.buyer_postcode = $event.target.value.replace(/\D/g, '')" placeholder="فقط عدد وارد کنید"
              style="padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; width: 100%; box-sizing: border-box;" />
          </div>
          <div style="display: flex; flex-direction: column; flex: 50%;">
            <label style="margin-bottom: 0.5rem; font-weight: bold;">تلفن خریدار:</label>
            <input v-model="form.buyer_phone" inputmode="numeric"
              @input="form.buyer_phone = $event.target.value.replace(/\D/g, '')" placeholder="فقط عدد وارد کنید"
              style="padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; width: 100%; box-sizing: border-box;" />
          </div>
        </div>
      </div>

      <!-- <div class="form-row">
        <label>نام فروشنده:</label>
        <input v-model="form.seller_name" readonly />
        <label>شماره اقتصادی فروشنده:</label>
        <input v-model="form.seller_economic_code" readonly />
        <label>شماره ثبت فروشنده:</label>
        <input v-model="form.seller_reg" readonly />
        <label>کد پستی فروشنده:</label>
        <input v-model="form.seller_postcode" readonly />
        <label>شناسه ملی فروشنده:</label>
        <input v-model="form.seller_national_id" readonly />
        <label>نشانی فروشنده:</label>
        <input v-model="form.seller_address" readonly />
        <label>تلفن فروشنده:</label>
        <input v-model="form.seller_phone" readonly />
      </div> -->
      <div class="input-table-container">
        <table class="input-table">
          <thead>
            <tr>
              <th style="width: 5%">ردیف</th>
              <th style="width: 7%">کد کالا</th>
              <th style="width: 28%">شرح کالا</th>
              <th style="width: 8%">مقدار</th>
              <th style="width: 8%">واحد</th>
              <th style="width: 9%">مبلغ واحد (ریال)</th>
              <th style="width: 12%">مبلغ کل (ریال)</th>
              <th style="width: 13%">جمع مالیات و عوارض ۱۰٪</th>
              <th style="width: 18%">جمع مبلغ کل و مالیات</th>
              <th style="width: 5%">حذف</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, idx) in form.items" :key="idx">
              <td>{{ idx + 1 }}</td>
              <td><input v-model="item.code" :readonly="true" /></td>
              <td><input v-model="item.description"
                  placeholder="برای افزودن کالا از گزینه 'دیدن ۱۰ فروش آخر' استفاده کنید" :readonly="true" /></td>
              <td><input type="number" v-model.number="item.quantity" @input="updateTotal(item)" min="0" step="1"
                  :readonly="true" /></td>
              <td><input v-model="item.unit" :readonly="true" /></td>
              <td><input type="number" v-model.number="item.price" @input="updateTotal(item)" min="0" step="1"
                  :readonly="true" /></td>
              <td>{{ formatNumber(item.total) }}</td>
              <td>{{ formatNumber(rowTax(item)) }}</td>
              <td>{{ formatNumber(rowWithTax(item)) }}</td>
              <td><button type="button" @click="removeItem(idx)">-</button></td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="form-actions">
        <button type="button" class="btn-action view-btn" @click="showLastSales">دیدن ۱۰ فروش آخر</button>
        <button type="button" class="btn-action save-buyer-btn" @click="saveBuyerInfo">ذخیره اطلاعات مشتری</button>
        <button type="button" class="btn-action view-buyers-btn" @click="showBuyersList">لیست مشتریان</button>
        <button type="submit" class="btn-action preview-btn">پیش نمایش</button>
        <button type="button" class="btn-action reset-btn" @click="resetForm">پاک کردن فرم</button>
        <button type="button" class="btn-action transfer-btn" @click="goToTransfer" v-if="isFormComplete">رفتن به
          حواله</button>
      </div>
    </form>
    <!-- Last Sales Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>۱۰ فروش آخر</h2>
          <button class="close-button" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <table class="modal-table">
            <thead>
              <tr>
                <th>تاریخ</th>
                <th>نام خریدار</th>
                <th>شماره فاکتور</th>
                <th>نوع</th>
                <th>گرماژ</th>
                <th>عرض</th>
                <th>تعداد رول</th>
                <th>وضعیت</th>
                <th>مقدار</th>
                <th>واحد</th>
                <th>مبلغ واحد (ریال)</th>
                <th>مبلغ کل (ریال)</th>
                <th>عملیات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="sale in lastSales" :key="sale.id">
                <td>{{ sale.date }}</td>
                <td>{{ sale.buyer_name }}</td>
                <td>{{ sale.invoice_number }}</td>
                <td>{{ translatePaperType(sale.items[0]?.type) || '-' }}</td>
                <td>{{ sale.items[0]?.gsm || '-' }}</td>
                <td>{{ sale.items[0]?.width || '-' }}</td>
                <td>{{ countReelsFromList(sale.list_of_reels) || sale.reel_count || '-' }}</td>
                <td>{{ translateStatus(sale.status) }}</td>
                <td>{{ sale.items[0]?.quantity || sale.total_weight }}</td>
                <td>کیلو</td>
                <td>{{ formatNumber(sale.items[0]?.price || 0) }}</td>
                <td>{{ formatNumber(sale.total_amount) }}</td>
                <td>
                  <button @click="selectSale(sale)" class="select-button">انتخاب</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Buyers List Modal -->
    <div v-if="showBuyersModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>لیست مشتریان</h2>
          <button class="close-button" @click="closeBuyersModal">&times;</button>
        </div>
        <div class="modal-body">
          <table v-if="buyersList.length > 0" class="modal-table">
            <thead>
              <tr>
                <th>نام خریدار</th>
                <th>شماره اقتصادی</th>
                <th>شماره ثبت</th>
                <th>کد ملی</th>
                <th>کد پستی</th>
                <th>نشانی</th>
                <th>تلفن</th>
                <th>عملیات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="buyer in buyersList" :key="buyer.buyer_name">
                <td>{{ buyer.buyer_name }}</td>
                <td>{{ buyer.buyer_economic_code }}</td>
                <td>{{ buyer.buyer_reg }}</td>
                <td>{{ buyer.buyer_national_id }}</td>
                <td>{{ buyer.buyer_postcode }}</td>
                <td>{{ buyer.buyer_address }}</td>
                <td>{{ buyer.buyer_phone }}</td>
                <td>
                  <button @click="selectBuyer(buyer)" class="select-button">انتخاب</button>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else class="empty-buyers-message">
            <p>لیست مشتریان خالی است.</p>
            <p>برای افزودن مشتری جدید، ابتدا اطلاعات مشتری را در فرم وارد کرده و سپس دکمه "ذخیره اطلاعات مشتری" را
              بزنید.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Invoice Preview for PDF -->
    <div ref="pdfPreview" v-if="showData" class="pdf-preview">
      <div class="invoice-container">
        <!-- شماره و تاریخ بالا سمت چپ -->
        <div class="header-row">
          <div class="fact-info fact-info-box">
            شماره فاکتور: {{ form.serial || '-' }}<br>
            تاریخ ثبت فاکتور: {{ form.date || '-' }}<br>
            تاریخ ثبت فروش: {{ form.sale_date || '-' }}
          </div>
        </div>
        <div class="invoice-title">صورت حساب فروش کالا</div>

        <!-- جدول مشخصات فروشنده -->
        <table class="info-table">
        <tbody>
          <tr>
            <th colspan="6" class="section-title">مشخصات فروشنده</th>
          </tr>
          <tr>
            <td>نام شرکت فروشنده</td>
            <td>کد اقتصادی</td>
            <td>شماره ثبت</td>
            <td>شناسه ملی</td>
            <td>کد پستی</td>
            <td>تلفن</td>
          </tr>
          <tr>
            <td>{{ form.seller_name }}</td>
            <td>{{ form.seller_economic_code }}</td>
            <td>{{ form.seller_reg }}</td>
            <td>{{ form.seller_national_id }}</td>
            <td>{{ form.seller_postcode }}</td>
            <td>{{ form.seller_phone }}</td>
          </tr>
          <tr>
            <td colspan="6"><b>نشانی:</b> {{ form.seller_address }}</td>
          </tr>
          </tbody>
        </table>

        <!-- جدول مشخصات خریدار -->
        <table class="info-table" style="margin-top: 18px;">
        <tbody>
          <tr>
            <th colspan="7" class="section-title">مشخصات خریدار</th>
          </tr>
          <tr>
            <td>نام شرکت خریدار</td>
            <td>شماره اقتصادی</td>
            <td>شماره ثبت</td>
            <td>کد ملی</td>
            <td>کد پستی</td>
            <td>تلفن</td>
          </tr>
          <tr>
            <td>{{ form.buyer_name || '-' }}</td>
            <td>{{ form.buyer_economic_code || '-' }}</td>
            <td>{{ form.buyer_reg || '-' }}</td>
            <td>{{ form.buyer_national_id || '-' }}</td>
            <td>{{ form.buyer_postcode || '-' }}</td>
            <td>{{ form.buyer_phone || '-' }}</td>
          </tr>
          <tr>
            <td colspan="7"><b>نشانی:</b> {{ form.buyer_address || '-' }}</td>
          </tr>
        </tbody>
        </table>

        <!-- جدول کالاها و جمع کل و مالیات و ... -->
        <table class="details-table" style="margin-top: 18px;">
          <thead>
            <tr>
              <th style="width: 5%">ردیف</th>
              <th style="width: 7%">کد کالا</th>
              <th style="width: 25%">شرح کالا</th>
              <th style="width: 8%">مقدار</th>
              <th style="width: 8%">واحد</th>
              <th style="width: 10%">مبلغ واحد (ریال)</th>
              <th style="width: 12%">مبلغ کل (ریال)</th>
              <th style="width: 11%">جمع مالیات و عوارض ۱۰٪</th>
              <th style="width: 16%">جمع مبلغ کل و مالیات</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, idx) in form.items" :key="idx">
              <td>{{ idx + 1 }}</td>
              <td>{{ item.code }}</td>
              <td>{{ item.description }}</td>
              <td>{{ item.quantity }}</td>
              <td>{{ item.unit }}</td>
              <td>{{ formatNumber(item.price) }}</td>
              <td>{{ formatNumber(item.total) }}</td>
              <td>{{ formatNumber(rowTax(item)) }}</td>
              <td>{{ formatNumber(rowWithTax(item)) }}</td>
            </tr>
          </tbody>
          <tfoot>
            <tr class="total-row">
              <td colspan="6" style="text-align: center;">جمع کل</td>
              <td>{{ formatNumber(totalAmount) }}</td>
              <td>{{ formatNumber(totalTax) }}</td>
              <td>{{ formatNumber(totalWithTax) }}</td>
            </tr>
          </tfoot>
        </table>

        <!-- بخش پایانی فاکتور -->
        <table class="footer-table standard-bordered-table">
        <tbody>
          <tr>
            <!-- ستون سمت راست: مهر و امضاءها -->
            <td class="footer-signs">
              <div class="signs-row">
                <div class="sign-box">مهر و امضاء خریدار</div>
                <div class="sign-box">مهر و امضاء فروشنده</div>
              </div>
            </td>
            <!-- ستون سمت چپ: مبالغ -->
            <td class="footer-amounts">
              <div class="amount-in-number">
                مبلغ قابل پرداخت به عدد: {{ formatNumber(totalWithTax) }}
              </div>
              <div class="amount-separator"></div>
              <div class="amount-in-words">
                مبلغ قابل پرداخت به حروف: {{ totalWithTaxInWords }}
              </div>
            </td>
          </tr>
        </tbody>
        </table>
      </div>
    </div>
    <button type="button" @click="printPreview" v-if="showData">دریافت PDF</button>

    <!-- Alert Modal -->
    <div v-if="showAlert" class="modal">
      <div class="modal-content alert-modal">
        <div class="modal-header">
          <h2>هشدار</h2>
          <button class="close-button" @click="handleAlertClose">&times;</button>
        </div>
        <div class="modal-body">
          <p>{{ alertMessage }}</p>
        </div>
        <div class="modal-footer">
          <button class="btn-action" @click="handleAlertClose">باشه</button>
        </div>
      </div>
    </div>

    <!-- Save Success Modal -->
    <div v-if="showSaveMessage" class="modal">
      <div class="modal-content save-message-modal">
        <div class="modal-header">
          <h2>موفق</h2>
          <button class="close-button" @click="showSaveMessage = false">&times;</button>
        </div>
        <div class="modal-body">
          <div class="message-icon">
            <i class="fas fa-check-circle"></i>
          </div>
          <p>اطلاعات مشتری با موفقیت ذخیره شد</p>
        </div>
        <div class="modal-footer">
          <button class="btn-action" @click="showSaveMessage = false">باشه</button>
        </div>
      </div>
    </div>
  </div>
        </section>
      </section>
    </teleport>
  </div>

</template>

<script>
import jalaali from 'jalaali-js';
import num2persian from "@/utils/num2persian";
import axios from 'axios';

// Configure axios
axios.defaults.baseURL = 'http://localhost:8000';

export default {
  name: 'SalesOrder',
  mounted() {
    document.title = 'SaleOrder';
  },
  data() {
    return {
      form: {
        serial: '',
        date: '',
        time: '',
        sale_date: '',
        buyer_name: '',
        buyer_economic_code: '',
        buyer_reg: '',
        buyer_postcode: '',
        buyer_phone: '',
        buyer_national_id: '',
        buyer_address: '',
        seller_name: 'شرکت صنایع تولیدی کاغذ و مقوای همایون',
        seller_economic_code: '14012603703',
        seller_reg: '',
        seller_national_id: '14012603703',
        seller_postcode: '3364146586',
        seller_address: 'کیلومتر ۱۵ جاده قدیم کرج - قزوین خیابان مرغک خیابان صنعت دومین کارخانه سمت چپ',
        seller_phone: '02644383368',
        license_number: '',
        plate_first: '',
        plate_letter: '',
        plate_second: '',
        plate_year: '',
        items: [
          { description: '', code: '', quantity: 1, unit: 'کیلو', price: 0, total: 0 }
        ]
      },
      showData: false,
      showModal: false,
      showBuyersModal: false,
      lastSales: [],
      buyersList: [],
      showAlert: false,
      alertMessage: '',
      lastBuyerName: '',
      showSaveMessage: false,
      nameMismatchWarning: '',
      isSelectingBuyer: false
    }
  },
  computed: {
    totalAmount() {
      return this.form.items.reduce((sum, item) => sum + Number(item.total || 0), 0);
    },
    totalTax() {
      return this.form.items.reduce((sum, item) => sum + Math.round((item.total || 0) * 0.10), 0);
    },
    totalWithTax() {
      return this.totalAmount + this.totalTax;
    },
    totalWithTaxInWords() {
      return num2persian(this.totalWithTax) + " ریال";
    },
    isFormComplete() {
      return this.form.serial &&
        this.form.buyer_name &&
        this.form.items.length > 0 &&
        this.form.items.every(item =>
          item.description &&
          item.quantity > 0 &&
          item.price > 0
        );
    }
  },
  methods: {
    getToday() {
      const today = new Date();
      const y = today.getFullYear();
      const m = String(today.getMonth() + 1).padStart(2, '0');
      const d = String(today.getDate()).padStart(2, '0');
      return `${y}/${m}/${d}`;
    },
    getTodayJalali() {
      const today = new Date();
      const { jy, jm, jd } = jalaali.toJalaali(today);
      return `${jy}/${String(jm).padStart(2, '0')}/${String(jd).padStart(2, '0')}`;
    },
    getCurrentTime() {
      const now = new Date();
      now.setMinutes(now.getMinutes() + 60);
      const h = String(now.getHours()).padStart(2, '0');
      const m = String(now.getMinutes()).padStart(2, '0');
      return `${h}:${m}`;
    },
    countReelsFromList(listOfReels) {
      if (!listOfReels || listOfReels.trim() === '') {
        return 0;
      }
      // شمارش تعداد رول‌ها بر اساس کاما
      const reels = listOfReels.split(',').filter(reel => reel.trim() !== '');
      return reels.length;
    },
    updateTotal(item) {
      item.total = (parseFloat(item.quantity) || 0) * (parseFloat(item.price) || 0);
    },
    addItem() {
      this.form.items.push({
        description: '',
        code: '',
        quantity: 1,
        unit: 'کیلو',
        price: 0,
        total: 0
      });
    },
    removeItem(idx) {
      this.form.items.splice(idx, 1);
    },
    submitForm() {
      this.form.date = this.getTodayJalali();
      this.form.time = this.getCurrentTime();
      this.showData = true;
    },
    formatNumber(val) {
      if (val == null || val === '') return '';
      return Number(val).toLocaleString('en-US', { minimumFractionDigits: 0 });
    },
    printPreview() {
      // Set custom filename for PDF
      const fileName = `SaleOrder${this.form.serial || 'NoNumber'}.pdf`;

      // Add a hidden input to set the filename
      const input = document.createElement('input');
      input.type = 'hidden';
      input.name = 'filename';
      input.value = fileName;
      document.body.appendChild(input);

      // Print the document
      window.print();

      // Remove the hidden input
      document.body.removeChild(input);
    },
    rowTax(item) {
      return Math.round((item.total || 0) * 0.10);
    },
    rowWithTax(item) {
      return Number(item.total || 0) + this.rowTax(item);
    },
    async showLastSales() {
      try {
        const response = await axios.get('/myapp/api/get_last_10_sales/');
        console.log('API Response:', response.data);
        this.lastSales = response.data;
        this.showModal = true;
      } catch (error) {
        console.error('Error details:', error.response || error);
        alert('خطا در دریافت اطلاعات فروش‌های اخیر');
      }
    },
    selectSale(sale) {
      // First check if this buyer exists in our buyers list
      const existingBuyer = this.buyersList.find(buyer =>
        buyer.buyer_name === sale.buyer_name
      );

      // Check if buyer names match between APIs
      if (this.form.buyer_name && this.form.buyer_name !== sale.buyer_name) {
        this.alertMessage = "نام خریدار انتخاب شده هماهنگ نیست. فرم بازنشانی می‌شود.";
        this.showAlert = true;
        this.resetForm();
        return;
      }

      if (existingBuyer) {
        // If buyer exists, use their complete information
        this.form.buyer_name = existingBuyer.buyer_name;
        this.form.buyer_economic_code = existingBuyer.buyer_economic_code;
        this.form.buyer_reg = existingBuyer.buyer_reg;
        this.form.buyer_national_id = existingBuyer.buyer_national_id;
        this.form.buyer_postcode = existingBuyer.buyer_postcode;
        this.form.buyer_address = existingBuyer.buyer_address;
        this.form.buyer_phone = existingBuyer.buyer_phone;
      } else {
        // If buyer doesn't exist, use basic information from sale
        this.form.buyer_name = sale.buyer_name;
        this.form.buyer_economic_code = sale.buyer_economic_code || '';
        this.form.buyer_reg = sale.buyer_reg || '';
        this.form.buyer_national_id = sale.buyer_national_id || '';
        this.form.buyer_postcode = sale.buyer_postcode || '';
        this.form.buyer_address = sale.buyer_address || '';
        this.form.buyer_phone = sale.buyer_phone || '';
      }

      // Store license plate information
      this.form.license_number = sale.license_number || '';
      this.form.plate_first = sale.plate_first || '';
      this.form.plate_letter = sale.plate_letter || '';
      this.form.plate_second = sale.plate_second || '';
      this.form.plate_year = sale.plate_year || '';

      // Set invoice number and sale date
      this.form.serial = sale.invoice_number || '';
      this.form.sale_date = sale.date || '';

      // Clear existing items
      this.form.items = [];
      console.log(sale.items && sale.items.length > 0)
      // Fill items with all details
      if (sale.items && sale.items.length > 0) {
        sale.items.forEach(item => {
          // Translate paper type to Persian
          let paperType = '';
          if (item.type === 'Testliner HOMAYOUN') {
            paperType = 'تست لاینر';
          } else if (item.type === 'Flutting HOMAYOUN') {
            paperType = 'فلوت';
          } else {
            paperType = item.type || '';
          }

          // Create description with proper format
          const description = `کاغذ ${paperType} ${sale.profile_name || ''} گرماژ ${item.gsm || ''} عرض ${item.width || ''}`;

          // شمارش تعداد رول‌ها از list_of_reels
          const reelCount = this.countReelsFromList(sale.list_of_reels);

          this.form.items.push({
            code: item.code || '',
            description: description,
            quantity: item.quantity,  // مقدار اصلی آیتم
            unit: item.unit || 'کیلو',
            price: item.price || 0,
            total: sale.total_weight || item.total || 0,
            gsm: item.gsm || '',
            width: item.width || '',
            weight: item.quantity || item.total || 0,  // استفاده از مقدار آیتم به عنوان وزن
            reelCount: reelCount || 0  // استفاده از مقدار آیتم
          });
          console.log('times:')
          console.log(this.form.items)
        });
      } else {
        // If no items, add one empty item
        const reelCount = this.countReelsFromList(sale.list_of_reels);

        this.form.items.push({
          code: '',
          description: '',
          quantity: sale.total_weight || 1,  // استفاده از وزن کل به عنوان مقدار
          unit: 'کیلو',
          price: 0,
          total: sale.total_weight || 0,
          gsm: '',
          width: '',
          weight: sale.total_weight || 0,  // استفاده از وزن کل
          reelCount: reelCount || 0  // استفاده از مقدار آیتم
        });
      }

      // Update totals for all items
      this.form.items.forEach(item => {
        this.updateTotal(item);
      });

      this.closeModal();
    },
    closeModal() {
      this.showModal = false;
    },
    translatePaperType(type) {
      const typeMap = {
        'Testliner HOMAYOUN': 'تست لاینر',
        'Flutting HOMAYOUN': 'فلوت'
      };
      return typeMap[type] || type;
    },
    translateStatus(status) {
      const statusMap = {
        'Office': 'دفتر',
        'Warehouse': 'انبار',
        'Loaded': 'بارگیری شده',
        'Unloaded': 'تخلیه شده',
        'Used': 'مصرف شده',
        'Moved': 'انتقال یافته',
        'Returned': 'برگشت خورده',
        'Cancelled': 'لغو شده',
        'Delivered': 'تحویل شده',
        'Pending': 'در انتظار',
        'Processing': 'در حال پردازش',
        'Completed': 'تکمیل شده'
      };
      return statusMap[status] || status;
    },
    async saveBuyerInfo() {
      try {
        // Check if buyer name is provided
        if (!this.form.buyer_name) {
          alert('لطفا نام خریدار را وارد کنید');
          return;
        }

        const response = await axios.post('/myapp/api/save_buyer_info/', this.form);
        console.log('Buyer info saved successfully:', response.data);

        // Add the current buyer to the buyersList
        const newBuyer = {
          buyer_name: this.form.buyer_name,
          buyer_economic_code: this.form.buyer_economic_code,
          buyer_reg: this.form.buyer_reg,
          buyer_national_id: this.form.buyer_national_id,
          buyer_postcode: this.form.buyer_postcode,
          buyer_address: this.form.buyer_address,
          buyer_phone: this.form.buyer_phone
        };

        // Add to the beginning of the list
        this.buyersList.unshift(newBuyer);

        this.showSaveMessage = true;
      } catch (error) {
        console.error('Error saving buyer info:', error.response || error);
        alert('خطا در ذخیره اطلاعات مشتری');
      }
    },
    async showBuyersList() {
      try {
        // If we already have buyers in the list, just show the modal
        if (this.buyersList.length > 0) {
          this.showBuyersModal = true;
          return;
        }

        const response = await axios.get('/myapp/api/get_buyers_list/');
        console.log('API Response:', response.data);
        this.buyersList = response.data;
        this.showBuyersModal = true;
      } catch (error) {
        console.error('Error details:', error.response || error);
        alert('خطا در دریافت لیست مشتریان');
      }
    },
    selectBuyer(buyer) {
      this.isSelectingBuyer = true;

      // Check if there's already a buyer name from last sales
      if (this.form.buyer_name && this.form.buyer_name !== buyer.buyer_name) {
        this.nameMismatchWarning = "نام خریدار انتخاب شده هماهنگ نیست";
        setTimeout(() => {
          this.nameMismatchWarning = '';
        }, 3000);
        return;
      }

      // Fill form with selected buyer data
      this.form.buyer_name = buyer.buyer_name;
      this.form.buyer_economic_code = buyer.buyer_economic_code;
      this.form.buyer_reg = buyer.buyer_reg;
      this.form.buyer_national_id = buyer.buyer_national_id;
      this.form.buyer_postcode = buyer.buyer_postcode;
      this.form.buyer_address = buyer.buyer_address;
      this.form.buyer_phone = buyer.buyer_phone;
      
      // Only add items if there are no existing items
      if (this.form.items.length === 0 || (this.form.items.length === 1 && !this.form.items[0].description)) {
        // Fill items with all details
        if (buyer.items && buyer.items.length > 0) {
          this.form.items = buyer.items.map(item => ({
            code: item.code || '',
            description: `${buyer.profile_name || item.description || ''} - ${item.net_weight || ''} - ${item.width || ''}`,
            quantity: item.quantity || 0,
            unit: item.unit || 'کیلو',
            price: item.price || 0,
            total: item.total || 0,
            gsm: item.gsm || '',
            width: item.width || '',
            weight: item.quantity || item.total || 0,
            reelCount: item.quantity
          }));
        } else {
          // If no items, add one empty item
          this.form.items = [{
            code: '',
            description: '',
            quantity: 1,
            unit: 'کیلو',
            price: 0,
            total: 0,
            gsm: '',
            width: '',
            weight: 0,
            reelCount: 0
          }];
        }

        // Update totals for all items
        this.form.items.forEach(item => {
          this.updateTotal(item);
        });
      }

      this.closeBuyersModal();
      this.isSelectingBuyer = false;
    },
    closeBuyersModal() {
      this.showBuyersModal = false;
    },
    resetForm() {
      // Reset form to initial state
      this.form = {
        serial: '',
        date: this.getTodayJalali(),
        time: this.getCurrentTime(),
        sale_date: '',
        buyer_name: '',
        buyer_economic_code: '',
        buyer_reg: '',
        buyer_postcode: '',
        buyer_phone: '',
        buyer_national_id: '',
        buyer_address: '',
        seller_name: 'شرکت صنایع تولیدی کاغذ و مقوای همایون',
        seller_economic_code: '14012603703',
        seller_reg: '',
        seller_national_id: '14012603703',
        seller_postcode: '3364146586',
        seller_address: 'کیلومتر ۱۵ جاده قدیم کرج - قزوین خیابان مرغک خیابان صنعت دومین کارخانه سمت چپ',
        seller_phone: '02644383368',
        license_number: '',
        plate_first: '',
        plate_letter: '',
        plate_second: '',
        plate_year: '',
        items: [
          { description: '', code: '', quantity: 1, unit: 'کیلو', price: 0, total: 0 }
        ]
      };
      this.showData = false;
    },
    async goToTransfer() {
      try {
        const transferData = {
          serial: this.form.serial,
          date: this.form.date,
          sale_date: this.form.sale_date,
          buyer_name: this.form.buyer_name,
          buyer_economic_code: this.form.buyer_economic_code,
          buyer_reg: this.form.buyer_reg,
          buyer_national_id: this.form.buyer_national_id,
          buyer_postcode: this.form.buyer_postcode,
          buyer_address: this.form.buyer_address,
          buyer_phone: this.form.buyer_phone,
          items: this.form.items.map(item => {
            // Extract gsm and width from description
            const gsmMatch = item.description.match(/گرماژ\s*(\d+)/);
            const widthMatch = item.description.match(/عرض\s*(\d+)/);

            return {
              code: item.code,
              name: item.description.split(' گرماژ')[0], // نام کالا
              description: item.description,
              quantity: item.reelCount,  // تعداد رول‌ها - استفاده از reelCount که در selectSale ذخیره شده
              unit: item.unit,
              price: item.price,
              total: item.total, // این وزن کل است
              gsm: gsmMatch ? gsmMatch[1] : '',
              width: widthMatch ? widthMatch[1] : '',
              weight: item.quantity || item.total || 0,  // استفاده از مقدار آیتم به عنوان وزن
              reelCount: item.reelCount  // انتقال تعداد رول‌ها
            };
          }),
          license_number: this.form.license_number || '',
          plate_first: this.form.plate_first || '',
          plate_letter: this.form.plate_letter || '',
          plate_second: this.form.plate_second || '',
          plate_year: this.form.plate_year || ''
        };

        // Save to localStorage
        localStorage.setItem('lastSaleData', JSON.stringify(transferData));

        // Navigate to transfer page
        this.$router.push('/myapp/invoice/havaleh');
      } catch (error) {
        console.error('Error preparing data for transfer:', error);
        alert('خطا در آماده‌سازی اطلاعات برای حواله');
      }
    },
    handleAlertClose() {
      this.showAlert = false;
      if (this.alertMessage.includes("فرم بازنشانی می‌شود")) {
        this.$router.push('/myapp/invoice/sales_order');
      }
    }
  },
  watch: {
    'form.buyer_name': function (newName) {
      if (this.isSelectingBuyer && this.lastBuyerName && newName && this.lastBuyerName !== newName) {
        this.nameMismatchWarning = "نام خریدار انتخاب شده هماهنگ نیست";
        setTimeout(() => {
          this.nameMismatchWarning = '';
        }, 3000);
      } else {
        this.lastBuyerName = newName;
      }
    },
    'form.serial': {
      handler(newValue) {
        if (newValue) {
          document.title = `SaleOrder - ${newValue}`;
        } else {
          document.title = 'SaleOrder';
        }
      },
      immediate: true
    }
  },
  created() {
    this.form.date = this.getTodayJalali();
    this.form.time = this.getCurrentTime();
  }
}
</script>

<style scoped>
@font-face {
  font-family: 'BNazanin';
  src: url('@/assets/fonts/BNazanin.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

.sales-order-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  direction: rtl;
  font-family: 'BNazanin', Arial, sans-serif;
}

.form-row {
  display: flex;
  gap: 15px;
  margin-bottom: 5px;
  flex-wrap: wrap;
  align-items: center;
}

.form-row label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.form-row input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 294px;
}

.input-table-container {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  margin: 0px 0;
  padding-bottom: 10px;
}

.input-table-container::-webkit-scrollbar {
  height: 8px;
}

.input-table-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.input-table-container::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.input-table-container::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.input-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  background: #fff;
}

.input-table th,
.input-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: center;
}

.input-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.input-table input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.input-table input[type="number"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.input-table input[type="number"]::-webkit-outer-spin-button,
.input-table input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.preview-btn {
  background-color: #FF9800;
  color: white;
}

.pdf-preview {
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
}

.invoice-container {
  width: 100%;
  margin: 30px auto;
  border: 2.5px solid #444;
  padding: 20px 8px 20px 8px;
  background: #fff;
  box-sizing: border-box;
  min-height: 900px;
  position: relative;
  font-size: 0.95em;
}

.header-row {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 10px;
  margin-top: 40px;
}

.header-row .fact-info {
  font-size: 1em;
  margin-left: 30px;
  text-align: left;
  margin-top: 10px;
}

.invoice-title {
  text-align: center;
  font-size: 1.6em;
  font-weight: bold;
  margin-top: 6px;
  margin-bottom: 10px;
  letter-spacing: 1px;
}

.party-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 18px;
}

.party-box {
  width: 49%;
  border: 1.5px solid #444;
  border-radius: 6px;
  padding: 10px 14px;
  background: #f7f7f7;
  font-size: 1em;
}

.party-title {
  font-weight: bold;
  margin-bottom: 6px;
  color: #222;
}

.party-box span {
  display: inline-block;
  min-width: 90px;
  font-weight: bold;
}

.details-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 0;
}

.details-table th,
.details-table td {
  border: 1.5px solid #444;
  padding: 5px 3px;
  text-align: center;
  font-size: 0.95em;
}

.details-table th {
  background: #e9ecef;
  font-weight: bold;
}

.details-table .total-row td {
  font-weight: bold;
  background: #f5f5f5;
  border-top: 2.5px solid #444;
  font-size: 1.1em;
}

.footer-section {
  margin-top: 30px;
  width: 100%;
}

.footer-section .amount-in-words {
  margin-bottom: 18px;
  font-size: 1em;
}

.footer-section .signatures {
  display: flex;
  justify-content: flex-end;
  gap: 60px;
  margin-top: 30px;
}

.footer-section .sign-box {
  border-top: 1.5px solid #444;
  width: 180px;
  text-align: center;
  padding-top: 8px;
  font-size: 1em;
}

/* Button Styles */
button {
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  border-radius: 4px;
  font-size: 1em;
  padding: 10px 20px;
  margin: 10px 0;
}

/* Add Row Button */
button[type="button"]:not(.preview-btn):not([v-if="showData"]) {
  background-color: #4CAF50;
  color: white;
}

button[type="button"]:not(.preview-btn):not([v-if="showData"]):hover {
  background-color: #45a049;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Download PDF Button */
button[type="button"][v-if="showData"] {
  background-color: #2196F3;
  color: white;
  font-size: 1.1em;
  padding: 12px 24px;
  margin: 20px 0;
}

button[type="button"][v-if="showData"]:hover {
  background-color: #1976D2;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Remove Item Button */
.input-table button {
  background-color: #ff4444;
  color: white;
  padding: 6px 12px;
  margin: 0;
  font-size: 0.9em;
}

.input-table button:hover {
  background-color: #cc0000;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

@media print {
  @page {
    size: A4 landscape;
    margin: 0;
  }

  body * {
    visibility: hidden;
  }

  .pdf-preview,
  .pdf-preview * {
    visibility: visible;
  }

  .pdf-preview {
    position: absolute;
    left: 0;
    top: 0;
    width: 297mm !important;
    height: 210mm !important;
    max-width: 297mm !important;
    max-height: 210mm !important;
    min-width: 297mm !important;
    min-height: 210mm !important;
    background: white !important;
    box-shadow: none !important;
    overflow: hidden !important;
    padding: 0 !important;
    margin: 0 !important;
    font-family: 'BNazanin', Arial, sans-serif !important;
  }

  button,
  .form-actions,
  form {
    display: none !important;
  }

  .pdf-preview,
  .invoice-container,
  .details-table,
  .info-table,
  .footer-table {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
    font-family: 'BNazanin', Arial, sans-serif !important;
  }

  .pdf-preview,
  .invoice-container {
    font-size: 0.9em !important;
  }

  body,
  .pdf-preview,
  .invoice-container,
  .info-table,
  .details-table,
  .footer-table,
  .fact-info-box {
    font-family: 'BNazanin', Arial, sans-serif !important;
  }

  .invoice-title {
    margin-top: 0 !important;
    margin-bottom: 2px !important;
  }

  .header-row {
    margin-top: 40px !important;
  }

  .info-table {
    margin-top: 2px !important;
    margin-bottom: 2px !important;
  }

  .details-table {
    margin-top: 4px !important;
  }

  .invoice-container {
    padding-top: 20px !important;
  }

  .header-row,
  .invoice-title,
  .info-table,
  .details-table {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
  }

  .invoice-container {
    padding-top: 0 !important;
    padding-bottom: 4px !important;
    margin-top: 0 !important;
  }

  .details-table th {
    background: #d1d1d1 !important;
  }

  .info-table .section-title {
    background: #d1d1d1 !important;
  }

  .fact-info-box {
    margin-top: 15px !important;
  }
}

.main-invoice-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  border: 2.5px solid #444;
  background: #fff;
  margin: 0 auto;
  font-size: 1em;
}

.section-title {
  font-weight: bold;
  font-size: 1.1em;
  margin-bottom: 8px;
  color: #222;
  text-align: right;
}

.info-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 0;
  border: 2.5px solid #444;
  background: #fff;
  margin-top: 18px;
}

.info-table th,
.info-table td {
  border: 1.5px solid #444;
  padding: 5px 3px;
  font-size: 0.95em;
  text-align: center;
  vertical-align: middle;
}

.info-table .section-title {
  background: #f2f2f2;
  font-weight: bold;
  text-align: center;
  font-size: 1.1em;
}

.fact-date-section {
  vertical-align: top;
  width: 220px;
  min-width: 180px;
}

.fact-box {
  border: 1.5px solid #444;
  border-radius: 8px;
  padding: 12px 18px;
  margin: 10px 0 0 0;
  background: #f7f7f7;
  font-size: 1.1em;
  text-align: right;
}

.seller-section,
.buyer-section {
  width: 50%;
  vertical-align: top;
  padding: 0 8px;
}

.details-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}

.details-table th,
.details-table td {
  border: 1.5px solid #444;
  padding: 5px 3px;
  text-align: center;
}

.details-table th {
  background: #e9ecef;
  font-weight: bold;
}

.details-table .total-row td {
  font-weight: bold;
  background: #f5f5f5;
  border-top: 2.5px solid #444;
  font-size: 1.1em;
}

.footer-section {
  margin-top: 30px;
  width: 100%;
}

.footer-section .amount-in-words {
  margin-bottom: 18px;
  font-size: 1em;
}

.footer-section .signatures {
  display: flex;
  justify-content: flex-end;
  gap: 60px;
  margin-top: 30px;
}

.footer-section .sign-box {
  border-top: 1.5px solid #444;
  width: 180px;
  text-align: center;
  padding-top: 8px;
  font-size: 1em;
}

.signatures-row {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 18px;
  margin-top: 40px;
}

.signatures-row .sign-box {
  border-top: 1.5px solid #444;
  width: 220px;
  text-align: right;
  padding-top: 8px;
  font-size: 1em;
  margin-bottom: 10px;
}

.amount-in-number,
.amount-in-words {
  font-size: 1.1em;
  margin-top: 18px;
  text-align: right;
  font-weight: bold;
}

.footer-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 0;
  margin-bottom: 0;
}

.footer-table td {
  vertical-align: top;
  padding: 18px 12px 12px 12px;
}

.footer-signs {
  width: 40%;
  min-width: 220px;
}

.footer-amounts {
  width: 60%;
  text-align: left;
  vertical-align: top;
}

.footer-signs .sign-box {
  border-top: none;
  width: 160px;
  text-align: center;
  padding-top: 8px;
  font-size: 1em;
  margin-bottom: 0;
}

.footer-amounts .amount-in-number,
.footer-amounts .amount-in-words {
  font-size: 1.1em;
  margin-bottom: 18px;
  text-align: right;
  font-weight: bold;
}

.footer-table.standard-bordered-table {
  width: 100%;
  border-collapse: collapse;
  border: 2.5px solid #444;
  margin-top: 0;
  margin-bottom: 0;
  direction: rtl;
  background: #fff;
}

.footer-table.standard-bordered-table td {
  border: 1.5px solid #444;
  vertical-align: top;
  padding: 18px 12px 12px 12px;
  text-align: right;
  background: #fff;
}

.footer-signs .signs-row {
  display: flex;
  flex-direction: row;
  gap: 40px;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 0;
}

.footer-signs .sign-box {
  /* حذف خط بالای هر sign-box */
  border-top: none;
  width: 160px;
  text-align: center;
  padding-top: 8px;
  font-size: 1em;
  margin-bottom: 0;
}

.amount-separator {
  border-top: 1.5px solid #444;
  margin: 12px 0;
  width: 100%;
}

.fact-info-box {
  border: 2.5px solid #444;
  border-radius: 8px;
  padding: 12px 18px;
  background: #fff;
  font-size: 1.1em;
  text-align: right;
  direction: rtl;
  display: inline-block;
  min-width: 220px;
  margin-bottom: 10px;
  margin-top: 15px;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 0px;
  margin-bottom: 0px;
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

.save-buyer-btn {
  background-color: #0922e0;
  color: white;
}

.save-buyer-btn:hover {
  background-color: #45a049;
}

.view-buyers-btn {
  background-color: #2196F3;
  color: white;
}

.view-buyers-btn:hover {
  background-color: #1976D2;
}

.reset-btn {
  background-color: #ff0000 !important;
  color: white;
}

.reset-btn:hover {
  background-color: #cc0000 !important;
}

.transfer-btn {
  background-color: #9c27b0;
  color: white;
}

.transfer-btn:hover {
  background-color: #7b1fa2;
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

/* Mobile Responsive Styles */
@media screen and (max-width: 768px) {
  .sales-order-container {
    margin: 10px;
    padding: 10px;
    width: auto;
    overflow-x: hidden;
  }

  .form-row {
    flex-direction: column;
    gap: 10px;

  }

  .form-row input {
    width: 100%;
    font-size: 16px;
    /* Prevent zoom on iOS */
  }

  .input-table-container {
    margin: 10px -10px;
    padding: 0 10px 10px 10px;
  }

  .input-table {
    min-width: 1000px;
  }

  .input-table th,
  .input-table td {
    white-space: nowrap;
    padding: 8px 4px;
  }

  .input-table input {
    min-width: 80px;
  }

  .form-actions {
    flex-direction: column;
    gap: 10px;
  }

  .btn-action {
    width: 100%;
    margin: 5px 0;
  }

  /* Modal Mobile Styles */
  .modal-content {
    width: 95%;
    margin: 10px;
    padding: 10px;
    max-height: 90vh;
  }

  .modal-table {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  .modal-table table {
    min-width: 1000px;
  }

  /* PDF Preview Mobile Styles */
  .pdf-preview {
    width: 100%;
    margin: 10px 0;
    padding: 5px;
  }

  .invoice-container {
    padding: 5px;
    margin: 10px 0;
  }

  .header-row {
    flex-direction: column;
    align-items: center;
  }

  .fact-info-box {
    width: 100%;
    margin: 5px 0;
  }

  .info-table,
  .details-table {
    font-size: 0.8em;
  }

  .footer-table.standard-bordered-table {
    font-size: 0.8em;
  }

  .footer-table td {
    padding: 10px 5px;
  }

  .footer-signs .signs-row {
    flex-direction: column;
    gap: 20px;
  }

  .footer-signs .sign-box {
    width: 100%;
  }
}

/* iPhone Specific Styles */
@supports (-webkit-touch-callout: none) {

  .form-row input,
  .input-table input {
    font-size: 16px;
    /* Prevent zoom on iOS */
  }

  .input-table,
  .modal-table {
    -webkit-overflow-scrolling: touch;
  }

  .modal-content {
    -webkit-overflow-scrolling: touch;
  }

  .pdf-preview {
    -webkit-overflow-scrolling: touch;
  }
}

.alert-modal {
  max-width: 400px !important;
  text-align: center;
}

.alert-modal .modal-header {
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
}

.alert-modal .modal-body {
  padding: 20px;
  font-size: 1.1em;
}

.alert-modal .modal-footer {
  padding-top: 15px;
  border-top: 1px solid #eee;
  text-align: center;
}

.alert-modal .btn-action {
  background-color: #2196F3;
  color: white;
  padding: 10px 30px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
}

.alert-modal .btn-action:hover {
  background-color: #1976D2;
}

.save-message-modal {
  max-width: 400px !important;
  text-align: center;
  border-top: 4px solid #4CAF50;
}

.save-message-modal .modal-header {
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
}

.save-message-modal .modal-body {
  padding: 20px;
  font-size: 1.1em;
}

.save-message-modal .modal-footer {
  padding-top: 15px;
  border-top: 1px solid #eee;
  text-align: center;
}

.save-message-modal .btn-action {
  background-color: #4CAF50;
  color: white;
  padding: 10px 30px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
}

.save-message-modal .btn-action:hover {
  background-color: #45a049;
}

.save-message-modal .message-icon {
  font-size: 48px;
  margin-bottom: 20px;
  color: #4CAF50;
}

.save-message-modal p {
  margin: 0;
  font-size: 1.2em;
  color: #333;
}

.name-warning {
  position: fixed;
  top: 20px;
  right: 20px;
  background-color: #f44336;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 1em;
  z-index: 1000;
  animation: fadeInOut 3s ease-in-out;
}

@keyframes fadeInOut {
  0% {
    opacity: 0;
    transform: translateY(-20px);
  }

  10% {
    opacity: 1;
    transform: translateY(0);
  }

  90% {
    opacity: 1;
    transform: translateY(0);
  }

  100% {
    opacity: 0;
    transform: translateY(-20px);
  }
}

.item-addition-message {
  text-align: center;
  color: #666;
  margin: 10px 0;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
  font-size: 1.1em;
}

.input-table input[readonly] {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.input-table input[readonly]::placeholder {
  color: #999;
  font-style: italic;
}

.page-title {
  text-align: center;
  font-size: 2em;
  color: #333;
  margin: 10px 0;
  font-weight: bold;
  font-family: 'BNazanin', Arial, sans-serif;
}

.empty-buyers-message {
  text-align: center;
  padding: 30px;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin: 20px 0;
}

.empty-buyers-message p:first-child {
  font-size: 1.2em;
  color: #666;
  margin-bottom: 10px;
}

.empty-buyers-message p:last-child {
  font-size: 1em;
  color: #888;
}
</style>