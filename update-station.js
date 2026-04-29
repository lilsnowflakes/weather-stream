// ============================================
// COC WEATHER STATION DATA UPDATER
// ============================================
// 
// HOW TO USE:
// 1. Go to: http://owc.enterprise.earthnetworks.com/onlineweathercenter.aspx?aid=3923
// 2. Wait for the page to fully load
// 3. Press F12 to open Developer Console
// 4. Paste this entire script into the Console
// 5. Press Enter
// 6. Copy the output and update your index.html
//
// ============================================

(function() {
  console.log('🌤️ COC Weather Station Data Extractor');
  console.log('=====================================\n');
  
  // Wait for page to load completely
  if (document.readyState !== 'complete') {
    console.log('⏳ Page still loading... Please wait and try again.');
    return;
  }
  
  // Function to extract text from element
  function getText(selector) {
    const element = document.querySelector(selector);
    if (element) {
      return element.textContent.trim();
    }
    return '--';
  }
  
  // Function to parse number from text
  function parseNum(text) {
    const num = parseFloat(text.replace(/[^0-9.-]/g, ''));
    return isNaN(num) ? 0 : num;
  }
  
  // Try to find data in various possible locations
  // Earth Networks uses different selectors depending on version
  
  const data = {
    temperature: parseNum(getText('#CurrentTemperature, .temperature, [data-field="temperature"]')),
    humidity: parseNum(getText('#CurrentHumidity, .humidity, [data-field="humidity"]')),
    windSpeed: parseNum(getText('#CurrentWindSpeed, .wind-speed, [data-field="windspeed"]')),
    dewPoint: parseNum(getText('#CurrentDewPoint, .dewpoint, [data-field="dewpoint"]')),
    pressure: parseNum(getText('#CurrentPressure, .pressure, [data-field="pressure"]')),
    rainfall: parseNum(getText('#CurrentRainfall, .rainfall, [data-field="precipitation"]'))
  };
  
  console.log('📊 Extracted Data:');
  console.log('Temperature:', data.temperature, '°F');
  console.log('Humidity:', data.humidity, '%');
  console.log('Wind Speed:', data.windSpeed, 'mph');
  console.log('Dew Point:', data.dewPoint, '°F');
  console.log('Pressure:', data.pressure, 'inHg');
  console.log('Rainfall:', data.rainfall, 'in\n');
  
  // Generate update code
  const updateCode = `
// ============================================
// UPDATED: ${new Date().toLocaleString('en-US', { timeZone: 'America/Los_Angeles' })} PST
// ============================================

const STATION_CONFIG = {
  manualData: {
    temperature: ${data.temperature},
    humidity: ${data.humidity},
    windSpeed: ${data.windSpeed},
    dewPoint: ${data.dewPoint},
    pressure: ${data.pressure},
    rainfall: ${data.rainfall}
  },
  
  location: { 
    lat: 34.4117,
    lon: -118.5698,
    name: 'College of the Canyons',
    stationId: 'CLLCN'
  }
};`;
  
  console.log('✅ Copy the code below and replace STATION_CONFIG in your index.html:\n');
  console.log('═'.repeat(70));
  console.log(updateCode);
  console.log('═'.repeat(70));
  
  // Try to copy to clipboard
  try {
    navigator.clipboard.writeText(updateCode).then(() => {
      console.log('\n✨ Code copied to clipboard! Paste it into your index.html');
    }).catch(() => {
      console.log('\n⚠️ Could not auto-copy. Please copy manually from above.');
    });
  } catch (e) {
    console.log('\n⚠️ Could not auto-copy. Please copy manually from above.');
  }
  
  // Alternative: Look for all possible data containers
  console.log('\n🔍 Debugging Info:');
  console.log('If data shows as 0 or --, try inspecting the page manually.');
  console.log('Look for elements containing the weather values and update selectors in this script.');
  
})();

// ============================================
// MANUAL EXTRACTION (if auto-extract fails)
// ============================================
// Look at the page and manually enter values:
//
// const STATION_CONFIG = {
//   manualData: {
//     temperature: 72,    // Enter from page
//     humidity: 45,       // Enter from page
//     windSpeed: 8,       // Enter from page
//     dewPoint: 58,       // Enter from page
//     pressure: 30.12,    // Enter from page
//     rainfall: 0.00      // Enter from page
//   },
//   location: { 
//     lat: 34.4117,
//     lon: -118.5698,
//     name: 'College of the Canyons',
//     stationId: 'CLLCN'
//   }
// };
