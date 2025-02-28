// imports
var cities = "your polygons should go here"
//------------------------------------------------------------

// 📌 Cargar la colección de ERA5-Land Horaria desde 1950
var era5_hourly = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY')
                   .select('temperature_2m')  // Seleccionar temperatura a 2m
                   .filter(ee.Filter.date('1950-01-01', '2024-12-31'));

// 🔄 Convertir la temperatura de Kelvin a Celsius
var era5_celsius = era5_hourly.map(function(img) {
  return img.subtract(273.15).copyProperties(img, ['system:time_start']);
});

// 🔹 Agrupar por fecha para obtener la media diaria correctamente
var uniqueDates = era5_celsius.aggregate_array('system:time_start')
                              .map(function(time) {
                                return ee.Date(time).format('YYYY-MM-dd');
                              }).distinct();

// 🔄 Generar imágenes diarias promediando las observaciones horarias
var era5_daily = ee.ImageCollection(uniqueDates.map(function(dateStr) {
  var date = ee.Date(dateStr);
  var dailyMean = era5_celsius.filterDate(date, date.advance(1, 'day')).mean(); // change this to min, max, median or any other stat
  return dailyMean.set('date', dateStr).set('system:time_start', date.millis());
}));

// 📊 Obtener estadísticas en cada ciudad
var statsCollection = era5_daily.map(function(img) {
  return img.reduceRegions({
    collection: cities,  // Capa de ciudades
    reducer: ee.Reducer.mean()
      .combine({reducer2: ee.Reducer.minMax(), sharedInputs: true})
      .combine({reducer2: ee.Reducer.stdDev(), sharedInputs: true}), // In this line we are getting the stats of the pixels inside the polygons but just with the mean selected before!
    scale: 10000,  // Ajusta según resolución deseada
    tileScale: 2   // Optimiza memoria
  }).map(function(feature) {
    return feature.set({
      'date': img.get('date'),  // Guardar la fecha
      'city': feature.get('NAME_LATN')  // Nombre de la ciudad
    });
  });
}).flatten();

// 📌 Exportar la serie completa a Google Drive en CSV
Export.table.toDrive({
  collection: statsCollection,
  description: 'City_Temperature_Stats_1950_2024_HourlyToDaily',
  fileFormat: 'CSV'
});
