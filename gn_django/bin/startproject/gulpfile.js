require('es6-promise').polyfill();

var gulp = require('gulp');
var path = require('path');
var less = require('gulp-less');
var autoprefixer = require('gulp-autoprefixer');
var minify = require('gulp-minify-css');
var util = require('gulp-util');
var execSync = require('child_process').execSync;
var merge = require('merge-stream');

gulp.task('compile', function () {
  // Grab the compilations list from our python project
  var compilations = JSON.parse(execSync('python manage.py get_less_compilations'));
  // Prepare our less compiler
  var l = less({});
  l.on('error',function(e){
    console.log(e);
    l.end();
  });
  // Extract the compilation tasks from the compilations list
  var compilationTasks = [];
  // Build task objects for each compilation
  for (var i = 0; i < compilations.length; i++) {
   var compilation = compilations[i];
   var task = gulp.src(compilation['source'])
    .pipe(l)
    .pipe(minify())
    .pipe(autoprefixer({
      browsers: ['last 10 versions']
    }))
    .pipe(gulp.dest(compilation['destination']));
    compilationTasks.push(task);
  }
  // Merge all of our compilation tasks in to a single merged task
  var mergedTask = compilationTasks[0];
  for (var i = 1; i < compilationTasks.length; i++) {
    mergedTask = merge(mergedTask, compilationTasks[i]);
  }
  return mergedTask;
});

gulp.task('watch', function () {
  // Grab the compilations list from our python project
  var compilations = JSON.parse(execSync('python manage.py get_less_compilations'));
  // Watch all of the less locations and run compile on file change
  var watchLocations = [];
  for (var i = 0; i < compilations.length; i++) {
    watchLocations.push(compilations[i]['watch']);
  }
  gulp.watch(watchLocations, ['compile']);
});

gulp.task('default', ['compile', 'watch']);
