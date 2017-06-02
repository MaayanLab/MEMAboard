

var about_string = 'Zoom, scroll, and click buttons to interact with the clustergram. <a href="http://amp.pharm.mssm.edu/clustergrammer/help"> <i class="fa fa-question-circle" aria-hidden="true"></i> </a>';
var hzome = ini_hzome();

function make_clust(inst_network) {

    CGM_on = true;
    FEAT_on = false;

    d3.select("#colorby paper-listbox").property("selected","None");

    console.log("inst_network",inst_network)
    d3.json('json/'+inst_network, function(network_data) {

      // define arguments object
      var args = {
        root: '#clustergram',
        'network_data': network_data,
        'about': about_string,
        'ini_expand': true, // this removes the sidebar
        // 'row_tip_callback': hzome.gene_info,
        // 'col_tip_callback':test_col_callback,
        // 'tile_tip_callback':test_tile_callback,
        // 'dendro_callback':dendro_callback, // USE THIS
        'matrix_update_callback': matrix_update_callback,
        'sidebar_width':150,
        'make_modals': false,
        // 'ini_view':{'N_row_var':20}
        // 'super_label_scale': 1.5,
        // 'row_label_scale': 1.0,
        // 'col_label_scale': 0.5,

      };

      resize_container(args);

      d3.select(window).on('resize',function() {
        resize_container(args);
        cgm.resize_viz();
      });

      d3.select(window).on()

      cgm = Clustergrammer(args);

      d3.select(".expand_button").remove()
      d3.select(cgm.params.root + ' .wait_message').remove();

      In(null, function() {} , 0); // This is really hacky but it works

  });

};

function make_clust_on_feature(inst_network) {

  CGM_on = true;
  FEAT_on = true;

  d3.json('json/'+inst_network, function(network_data) {

          // define arguments object
      var args = {
        root: '#clustergram',
        'network_data': network_data,
        'about': about_string,
        'ini_expand': true, // this removes the sidebar
        // 'row_tip_callback':hzome.gene_info,
        // 'col_tip_callback':test_col_callback,
        // 'tile_tip_callback':test_tile_callback,
        // 'dendro_callback':dendro_callback, // USE THIS
        'matrix_update_callback': matrix_update_callback,
        'sidebar_width':150,
        'make_modals': false,
        // 'ini_view':{'N_row_var':20}
        // 'super_label_scale': 1.5,
        // 'row_label_scale': 1.0,
        // 'col_label_scale': 0.5,

      };

      resize_container(args);

      d3.select(window).on('resize',function() {
        resize_container(args);
        cgm.resize_viz();
      });

      d3.select(window).on()

      cgm = Clustergrammer(args);

      d3.select(".expand_button").remove()
      d3.select(cgm.params.root + ' .wait_message').remove();

      In(null, function() {} , 0);
  });

};

function resize_container(args){

  var screen_width = d3.select(".stage").style("width")
  var screen_height = d3.select(".stage").style("height");

  // console.log("resizing",screen_width, screen_height)

  d3.select(args.root)
    .style('width', screen_width)
    .style('height', screen_height);
};

function dendro_callback(dendro_data) {
  console.log("dendro_callback")
  console.log(dendro_data)
  console.log(dendro_data.__data__) // use this to get data from 
};

function filterClustergram(names) {
 
  clearTimeout(timer);

  timer = setTimeout(function() {
    if (names.length == 0) {
      var selection = {}; // GET ALL ROWS
    } else {
      var selection = { 'row' : names.map(function(x) { return x.replace("_"," ")}) };
    };
    cgm.filter_viz_using_names(selection);
  }, 500);
};

function prepare_clustergram() {
  // Fly out scatter, fly in clustergram
  d3.select("#scatter").style("visibility","hidden");
  d3.select(".ink-panel-menubar").style("display","none");
  d3.select("#clustergram").style("display","block");
  // Remove expand button
  d3.select(".expand_button").remove()
  // Change left menubar options
  d3.select("#labelby").style("display","none");
  d3.select("#colorby").attr("label", "Cluster by feature");

  // var opt = d3.select("#colorby paper-listbox").property("selected");
  // if (['ECMp','Ligand'].indexOf(opt) > -1) {
  //   d3.select("#colorby paper-listbox").property("selected","None");
  // };

  d3.selectAll("#ECMp, #Ligand").style("display","none");
  d3.select("#normalize-data-checkbox").style("display","none");
  d3.selectAll(".item").style("display","none");
  // Change help button
  d3.select(".main.scatter").style("display","none");
  d3.select(".main.clustergram").style("display","block");

};

function prepare_scatter() {
  // Fly out clustergram, fly in scatter
  d3.select("#clustergram").style("display","none");
  d3.select(".ink-panel-menubar").style("display","flex");
  d3.select("#scatter").style("visibility","visible");
  // Change left menubar options
  d3.select("#labelby").style("display","block");
  d3.select("#colorby").attr("label", "Color by");
  d3.selectAll("#ECMp, #Ligand").style("display","flex");
  d3.select("#normalize-data-checkbox").style("display","block");
  d3.selectAll(".item").style("display","flex");
  // Change help button
  d3.select(".main.scatter").style("display","block");
  d3.select(".main.clustergram").style("display","none");

  // var handler = window.onresize;
  // handler();
};

function delete_clustergram() {
  d3.selectAll("#clustergram div").remove();
  CGM_on = false;
};

// Do this every time the clustergram updates
function matrix_update_callback() {
  d3.select(".expand_button").remove();
};

