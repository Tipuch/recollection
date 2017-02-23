'use strict';
var gulp = require('gulp');
var sass = require('gulp-ruby-sass');

// load plugins
var $ = require('gulp-load-plugins')();
var gutil = require('gulp-util');
var runSequence = require('run-sequence');
var pjson = require('./package.json');
var plumber = require('gulp-plumber');

var src_path = "build/";
var dest_path = "../apps/words/static/words/";

// paths to resources
var paths = {
  scss: src_path + 'scss/**/*.scss',
  scripts: src_path + 'js/**/*.js',
  main: src_path + 'js/main.js',
  plugins: [''],
  cssvendors: [
  // Load Bootstrap
  'node_modules/bootstrap-sass/assets/stylesheets/bootstrap.scss',
  // Fontawesome
  'node_modules/font-awesome/scss/font-awesome.scss'
  ],
  fontsvendors: ['node_modules/font-awesome/fonts/fontawesome-webfont.ttf', 'node_modules/font-awesome/fonts/fontawesome-webfont.woff',
            'node_modules/font-awesome/fonts/fontawesome-webfont.woff2', 'node_modules/font-awesome/fonts/fontawesome-webfont.eot', 'node_modules/font-awesome/fonts/fontawesome-webfont.svg']
};

// destinations for resources
var dest = {
  css: dest_path + 'css/',
  scripts: dest_path + 'js/',
  fonts: dest_path + 'fonts/'
};

// process scss file
gulp.task('styles', function () {
  return sass(paths.scss, {
      precision: 10
    })
    .on('error', sass.logError)
    .pipe(gulp.dest(dest.css))
    ;
});

// process vendors scss file
gulp.task('styles_vendors', function () {
  return sass(paths.cssvendors, {
      precision: 10
    })
    .pipe($.concat('vendors.css'))
    .pipe($.rename('vendors.css'))
    .on('error', sass.logError)
    .pipe(gulp.dest(dest.css))
    ;
});

// Combine vendors js, concat, rename, move
gulp.task('jsvendors', function(){
  return gulp.src(paths.vendors)
    .pipe($.concat('vendors.js'))
    .pipe($.rename('vendors.js'))
    .pipe(gulp.dest(dest.scripts))
});

gulp.task('fonts_vendors',function(){
   return gulp.src(paths.fontsvendors)
       .pipe(gulp.dest(dest.fonts))
});

// Clean up dist and temporary
gulp.task('clean', function(){
  return gulp.src(['.tmp', 'dist'], { read: false }).pipe($.clean());
});

gulp.task('build', ['styles', 'styles_vendors', 'jsvendors', 'fonts_vendors']);

gulp.task('default', ['clean'], function(){
  gulp.start('build');
});


gulp.task('watch', function(){
  gulp.watch(paths.scss, ['styles']);
  gulp.watch(paths.cssvendors, ['styles_vendors'])
});