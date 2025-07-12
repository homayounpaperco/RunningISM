<script>
export default {
  name: "licenseNumber",
  props: ['lic'],
  computed: {
    parsedLicense() {
      return this.parseLicenseNumber(this.lic);
    }
  },
  methods: {
    parseLicenseNumber(licenseNumber) {
      // Define a regex pattern to match the parts of the license number
      const regex = /^(\d{2})(\w)(\d{3})(\w{5})(\d{2})$/;
      const matches = licenseNumber.match(regex);
      
      if (matches) {
        // Extract the matched groups
        const first = matches[1];
        const letter = matches[2];
        const second = matches[3];
        const year = matches[5];

        // Create an object with the parsed values
        return {
          first: first,
          letter: letter,
          second: second,
          country: 'ایران',
          year: year
        };
      }
      
      // Fallback: if regex doesn't match, try string slicing
      if (licenseNumber && licenseNumber.length >= 8) {
        const first = licenseNumber.slice(0, 2);
        const letter = licenseNumber.slice(2, 3);
        const second = licenseNumber.slice(3, 6);
        const year = licenseNumber.slice(-2);

        return {
          first: first,
          letter: letter,
          second: second,
          country: 'ایران',
          year: year
        };
      }
      
      // Return default values if parsing fails
      return {
        first: '',
        letter: '',
        second: '',
        country: 'ایران',
        year: ''
      };
    }
  }
}
</script>

<template>
  <div class="flex flex-row justify-center">
    <div class="rounded-lg bg-white shadow-lg w-44 h-12 overflow-hidden">
      <div class="flex rounded-lg border-2 border-black shadow h-full">
        <!-- Left section - Country and Year -->
        <div class="flex flex-none flex-col items-center justify-center px-1 border-e-2 border-black font-bold text-xs w-12 text-black">
          <span class="text-xs leading-tight">ایران</span>
          <span class="text-xs leading-tight">{{ parsedLicense.year }}</span>
        </div>
        
        <!-- Center section - License numbers -->
        <div class="flex-grow flex flex-row gap-1 justify-center items-center font-mono text-base font-bold px-2 text-black">
          <span class="min-w-0 flex-shrink-0">{{ parsedLicense.second }}</span>
          <span class="min-w-0 flex-shrink-0">{{ parsedLicense.letter }}</span>
          <span class="min-w-0 flex-shrink-0">{{ parsedLicense.first }}</span>
        </div>
        
        <!-- Right section - Flag and IR -->
        <div class="flex flex-none flex-col items-end justify-center px-1 bg-blue-600 border-s-2 border-black text-white text-xs font-bold w-8">
          <img src="@/assets/Flag_of_Iran.svg.png" class="h-3 mb-1">
          <span class="text-xs leading-tight">.I.R</span>
        </div>
      </div>
    </div>
  </div>
</template>

