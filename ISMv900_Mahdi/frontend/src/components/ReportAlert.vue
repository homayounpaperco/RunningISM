<script>
import { initFlowbite } from 'flowbite'

export default {
 name: "ReportAlert",
 props: ['msg', 'id'],
 mounted() {
    initFlowbite();
 },
 data(){
    return{
      hide: false
    }
 },
 methods: {
    closeAlert() {
      // this.hide = true;
      const params = {
        'id': this.id,
      }

      this.axios.post('/myapp/api/alertsResolve', {params: params}, {params: params}).then((response) => {
        console.log(response)
        // if (response.status == 200) {
        // }
      }).catch((error) => {
        console.error("Login failed:", error); // Log errors for debugging
      });
    }
 }
}
</script>

<template>
    <div class="w-full max-h-full" v-if="!hide">
      <div id="toast-danger" class="flex flex-col gap-2 w-full max-w-xs p-4 mb-4 text-gray-500 bg-white rounded-lg shadow dark:text-gray-400 dark:bg-gray-800" role="alert">
          <header class="flex flex-row justify-between items-center gap-2">
            <div class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-red-500 bg-red-100 rounded-lg dark:bg-red-800 dark:text-red-200">
              <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 11.793a1 1 0 1 1-1.414 1.414L10 11.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 10 6.293 7.707a1 1 0 0 1 1.414-1.414L10 8.586l2.293-2.293a1 1 0 0 1 1.414 1.414L11.414 10l2.293 2.293Z"/>
              </svg>
              <span class="sr-only">Error icon</span>
            </div>
            <p>هشدار!</p>
            <button type="button" class="ms-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex items-center justify-center h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700" @click="closeAlert" aria-label="Close">
              <span class="sr-only">Close</span>
              <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
              </svg>
            </button>
          </header>
          <main class="flex justify-start text-sm font-normal px-2">
            <p>{{ msg }}</p>
          </main>
      </div>
    </div>
</template>
