<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1" />
<meta name="generator" content="pdoc 0.10.0" />
<title>transposonmapper.importing API documentation</title>
<meta name="description" content="" />
<link rel="preload stylesheet" as="style" href="https://cdnjs.cloudflare.com/ajax/libs/10up-sanitize.css/11.0.1/sanitize.min.css" integrity="sha256-PK9q560IAAa6WVRRh76LtCaI8pjTJ2z11v0miyNNjrs=" crossorigin>
<link rel="preload stylesheet" as="style" href="https://cdnjs.cloudflare.com/ajax/libs/10up-sanitize.css/11.0.1/typography.min.css" integrity="sha256-7l/o7C8jubJiy74VsKTidCy1yBkRtiUGbVkYBylBqUg=" crossorigin>
<link rel="stylesheet preload" as="style" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/styles/github.min.css" crossorigin>
<style>:root{--highlight-color:#fe9}.flex{display:flex !important}body{line-height:1.5em}#content{padding:20px}#sidebar{padding:30px;overflow:hidden}#sidebar > *:last-child{margin-bottom:2cm}.http-server-breadcrumbs{font-size:130%;margin:0 0 15px 0}#footer{font-size:.75em;padding:5px 30px;border-top:1px solid #ddd;text-align:right}#footer p{margin:0 0 0 1em;display:inline-block}#footer p:last-child{margin-right:30px}h1,h2,h3,h4,h5{font-weight:300}h1{font-size:2.5em;line-height:1.1em}h2{font-size:1.75em;margin:1em 0 .50em 0}h3{font-size:1.4em;margin:25px 0 10px 0}h4{margin:0;font-size:105%}h1:target,h2:target,h3:target,h4:target,h5:target,h6:target{background:var(--highlight-color);padding:.2em 0}a{color:#058;text-decoration:none;transition:color .3s ease-in-out}a:hover{color:#e82}.title code{font-weight:bold}h2[id^="header-"]{margin-top:2em}.ident{color:#900}pre code{background:#f8f8f8;font-size:.8em;line-height:1.4em}code{background:#f2f2f1;padding:1px 4px;overflow-wrap:break-word}h1 code{background:transparent}pre{background:#f8f8f8;border:0;border-top:1px solid #ccc;border-bottom:1px solid #ccc;margin:1em 0;padding:1ex}#http-server-module-list{display:flex;flex-flow:column}#http-server-module-list div{display:flex}#http-server-module-list dt{min-width:10%}#http-server-module-list p{margin-top:0}.toc ul,#index{list-style-type:none;margin:0;padding:0}#index code{background:transparent}#index h3{border-bottom:1px solid #ddd}#index ul{padding:0}#index h4{margin-top:.6em;font-weight:bold}@media (min-width:200ex){#index .two-column{column-count:2}}@media (min-width:300ex){#index .two-column{column-count:3}}dl{margin-bottom:2em}dl dl:last-child{margin-bottom:4em}dd{margin:0 0 1em 3em}#header-classes + dl > dd{margin-bottom:3em}dd dd{margin-left:2em}dd p{margin:10px 0}.name{background:#eee;font-weight:bold;font-size:.85em;padding:5px 10px;display:inline-block;min-width:40%}.name:hover{background:#e0e0e0}dt:target .name{background:var(--highlight-color)}.name > span:first-child{white-space:nowrap}.name.class > span:nth-child(2){margin-left:.4em}.inherited{color:#999;border-left:5px solid #eee;padding-left:1em}.inheritance em{font-style:normal;font-weight:bold}.desc h2{font-weight:400;font-size:1.25em}.desc h3{font-size:1em}.desc dt code{background:inherit}.source summary,.git-link-div{color:#666;text-align:right;font-weight:400;font-size:.8em;text-transform:uppercase}.source summary > *{white-space:nowrap;cursor:pointer}.git-link{color:inherit;margin-left:1em}.source pre{max-height:500px;overflow:auto;margin:0}.source pre code{font-size:12px;overflow:visible}.hlist{list-style:none}.hlist li{display:inline}.hlist li:after{content:',\2002'}.hlist li:last-child:after{content:none}.hlist .hlist{display:inline;padding-left:1em}img{max-width:100%}td{padding:0 .5em}.admonition{padding:.1em .5em;margin-bottom:1em}.admonition-title{font-weight:bold}.admonition.note,.admonition.info,.admonition.important{background:#aef}.admonition.todo,.admonition.versionadded,.admonition.tip,.admonition.hint{background:#dfd}.admonition.warning,.admonition.versionchanged,.admonition.deprecated{background:#fd4}.admonition.error,.admonition.danger,.admonition.caution{background:lightpink}</style>
<style media="screen and (min-width: 700px)">@media screen and (min-width:700px){#sidebar{width:30%;height:100vh;overflow:auto;position:sticky;top:0}#content{width:70%;max-width:100ch;padding:3em 4em;border-left:1px solid #ddd}pre code{font-size:1em}.item .name{font-size:1em}main{display:flex;flex-direction:row-reverse;justify-content:flex-end}.toc ul ul,#index ul{padding-left:1.5em}.toc > ul > li{margin-top:.5em}}</style>
<style media="print">@media print{#sidebar h1{page-break-before:always}.source{display:none}}@media print{*{background:transparent !important;color:#000 !important;box-shadow:none !important;text-shadow:none !important}a[href]:after{content:" (" attr(href) ")";font-size:90%}a[href][title]:after{content:none}abbr[title]:after{content:" (" attr(title) ")"}.ir a:after,a[href^="javascript:"]:after,a[href^="#"]:after{content:""}pre,blockquote{border:1px solid #999;page-break-inside:avoid}thead{display:table-header-group}tr,img{page-break-inside:avoid}img{max-width:100% !important}@page{margin:0.5cm}p,h2,h3{orphans:3;widows:3}h1,h2,h3,h4,h5,h6{page-break-after:avoid}}</style>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/highlight.min.js" integrity="sha256-Uv3H6lx7dJmRfRvH8TH6kJD1TSK1aFcwgx+mdg3epi8=" crossorigin></script>
<script>window.addEventListener('DOMContentLoaded', () => hljs.initHighlighting())</script>
</head>
<body>
<main>
<article id="content">
<header>
<h1 class="title">Module <code>transposonmapper.importing</code></h1>
</header>
<section id="section-intro">
<details class="source">
<summary>
<span>Expand source code</span>
</summary>
<pre><code class="python">from .verify_data_files import verify_data_files
from .load_default_files import load_default_files,load_sgd_tab
from .read_genes import read_genes


__all__ = [
    &#34;load_default_files&#34;,
    &#34;read_genes&#34;,
    &#34;load_sgd_tab&#34;
]</code></pre>
</details>
</section>
<section>
<h2 class="section-title" id="header-submodules">Sub-modules</h2>
<dl>
<dt><code class="name"><a title="transposonmapper.importing.verify_data_files" href="verify_data_files.html">transposonmapper.importing.verify_data_files</a></code></dt>
<dd>
<div class="desc"></div>
</dd>
</dl>
</section>
<section>
</section>
<section>
<h2 class="section-title" id="header-functions">Functions</h2>
<dl>
<dt id="transposonmapper.importing.load_default_files"><code class="name flex">
<span>def <span class="ident">load_default_files</span></span>(<span>gff_file=None, essentials_file=None, gene_names_file=None)</span>
</code></dt>
<dd>
<div class="desc"><p>This function loads some files that have a recurrent use throughout the pipeline.
It will look inside the satay/data_files folder for the files if the input is None.
Otherwise it will return the same input file.
</p>
<pre><code>Usage:
------
file1, file2, file3=load_default_files(gff_file=file1,
                                        essentials_file=file2,
                                        gene_names_file=file3)
if you dont provide a specific file as an input , then it will look into the default folder
satay/data_files/ and it will give the standard file provided in the package.

file1, file2, file3=load_default_files(gff_file=None,
                                        essentials_file=None,
                                        gene_names_file=None)

Parameters
----------
gff_file : [.gff3] --&gt; Annotated genome from Saccharomyces cerevisiae (baker's yeast) 
    (&lt;https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/146/045/GCF_000146045.2_R64/GCF_000146045.2_R64_genomic.gff.gz&gt;)
essentials_file : [.txt] --&gt;  Essentials genes annotated from yeast , written using the systematic name standard , 
    all in one column
gene_names_file : [.txt] --&gt; This documents lists all the Saccharomyces cerevisiae S288c entries present in
</code></pre>
<p>this release of UniProtKB/Swiss-Prot. Yeast (Saccharomyces cerevisiae): entries, gene names and cross-references to SGD.
Release:
2021_01 of 10-Feb-2021</p>
<pre><code>Returns
-------
gff_file : [.gff3]--&gt; Annotated genome from Saccharomyces cerevisiae (baker's yeast) 
    (&lt;https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/146/045/GCF_000146045.2_R64/GCF_000146045.2_R64_genomic.gff.gz&gt;)
essentials_file : [.txt]--&gt;  Essentials genes annotated from yeast , written using the systematic name standard , 
    all in one column
gene_names_file : [.txt]--&gt; This documents lists all the Saccharomyces cerevisiae S288c entries present in
</code></pre>
<p>this release of UniProtKB/Swiss-Prot. Yeast (Saccharomyces cerevisiae): entries, gene names and cross-references to SGD.
Release:
2021_01 of 10-Feb-2021</p></div>
<details class="source">
<summary>
<span>Expand source code</span>
</summary>
<pre><code class="python">def load_default_files(gff_file=None, essentials_file=None, gene_names_file=None):
    &#34;&#34;&#34;This function loads some files that have a recurrent use throughout the pipeline.
    It will look inside the satay/data_files folder for the files if the input is None. 
    Otherwise it will return the same input file.  
    
    Usage:
    ------
    file1, file2, file3=load_default_files(gff_file=file1,
                                            essentials_file=file2,
                                            gene_names_file=file3)
    if you dont provide a specific file as an input , then it will look into the default folder
    satay/data_files/ and it will give the standard file provided in the package.

    file1, file2, file3=load_default_files(gff_file=None,
                                            essentials_file=None,
                                            gene_names_file=None)

    Parameters
    ----------
    gff_file : [.gff3] --&gt; Annotated genome from Saccharomyces cerevisiae (baker&#39;s yeast) 
        (https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/146/045/GCF_000146045.2_R64/GCF_000146045.2_R64_genomic.gff.gz)
    essentials_file : [.txt] --&gt;  Essentials genes annotated from yeast , written using the systematic name standard , 
        all in one column
    gene_names_file : [.txt] --&gt; This documents lists all the Saccharomyces cerevisiae S288c entries present in
this release of UniProtKB/Swiss-Prot. Yeast (Saccharomyces cerevisiae): entries, gene names and cross-references to SGD. 
             Release:     2021_01 of 10-Feb-2021

    Returns
    -------
    gff_file : [.gff3]--&gt; Annotated genome from Saccharomyces cerevisiae (baker&#39;s yeast) 
        (https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/146/045/GCF_000146045.2_R64/GCF_000146045.2_R64_genomic.gff.gz)
    essentials_file : [.txt]--&gt;  Essentials genes annotated from yeast , written using the systematic name standard , 
        all in one column
    gene_names_file : [.txt]--&gt; This documents lists all the Saccharomyces cerevisiae S288c entries present in
this release of UniProtKB/Swiss-Prot. Yeast (Saccharomyces cerevisiae): entries, gene names and cross-references to SGD. 
             Release:     2021_01 of 10-Feb-2021
    &#34;&#34;&#34;

    default_path = pkg_resources.resource_filename(&#34;transposonmapper&#34;, &#34;data_files/&#34;)
    if gff_file is None:
        gff_file = os.path.join(
            default_path, &#34;Saccharomyces_cerevisiae.R64-1-1.99.gff3&#34;
        )
    if essentials_file is None:
        essentials_file = os.path.join(
            default_path, &#34;Cerevisiae_AllEssentialGenes_List.txt&#34;
        )
    if gene_names_file is None:
        gene_names_file = os.path.join(default_path, &#34;Yeast_Protein_Names.txt&#34;)


    return gff_file, essentials_file, gene_names_file</code></pre>
</details>
</dd>
<dt id="transposonmapper.importing.load_sgd_tab"><code class="name flex">
<span>def <span class="ident">load_sgd_tab</span></span>(<span>sgd_features_file=None)</span>
</code></dt>
<dd>
<div class="desc"><p>This function loads the file SGD_features.tab
The latest version of the SGD_features.tab file is based on Genome Version R64-2-1.
If a specific file is provided it will output that file , otherwise , if it is set to None then
it will give the standard file provided in the package.
Usage:
file1=load_sgd_tab(sgd_features_file=file1)
if you dont provide a specific file as an input , then it will look into the default folder
satay/data_files/ and it will give the standard file provided in the package.</p>
<p>file1=load_sgd_tab(sgd_features_file=None)</p>
<h2 id="arguments">Arguments</h2>
<p>sgd_features_file {.gff3} &ndash; The latest version of the SGD_features.tab file is based on Genome Version R64-2-1.</p>
<h2 id="returns">Returns</h2>
<p>sgd_features_file {.gff3} &ndash; The latest version of the SGD_features.tab file is based on Genome Version R64-2-1.</p></div>
<details class="source">
<summary>
<span>Expand source code</span>
</summary>
<pre><code class="python">def load_sgd_tab(sgd_features_file=None):
    &#34;&#34;&#34;This function loads the file SGD_features.tab
    The latest version of the SGD_features.tab file is based on Genome Version R64-2-1.
    If a specific file is provided it will output that file , otherwise , if it is set to None then 
    it will give the standard file provided in the package. 
    Usage:
    file1=load_sgd_tab(sgd_features_file=file1)
    if you dont provide a specific file as an input , then it will look into the default folder
    satay/data_files/ and it will give the standard file provided in the package.

    file1=load_sgd_tab(sgd_features_file=None)
    
   
    Arguments:
        sgd_features_file {.gff3} -- The latest version of the SGD_features.tab file is based on Genome Version R64-2-1.

    Returns:
        sgd_features_file {.gff3} -- The latest version of the SGD_features.tab file is based on Genome Version R64-2-1.
    &#34;&#34;&#34;
    default_path = pkg_resources.resource_filename(&#34;transposonmapper&#34;, &#34;data_files/&#34;)
    if sgd_features_file is None: 

        sgd_features_file = os.path.join(default_path,&#39;SGD_features.tab&#39;)

    return sgd_features_file</code></pre>
</details>
</dd>
<dt id="transposonmapper.importing.read_genes"><code class="name flex">
<span>def <span class="ident">read_genes</span></span>(<span>gff_file, essentials_file, gene_names_file)</span>
</code></dt>
<dd>
<div class="desc"><p>This function reads the useful information inside the gff_file, essentials_file and
gene_names_file.
For the gff_file and essentials_file extracts the gene coordinates , specifying the chromosome, start ,end
and direction.
For the gene_names_files it translates the systematic name into the standard name.</p>
<pre><code>Usage:

 [gene_coordinates, essential_coordinates, aliases_designation] = 
        read_genes(gff_file, essentials_file, gene_names_file)

Inputs:
    - gff_file : Annotated genome from Saccharomyces cerevisiae (baker's yeast) (&lt;https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/146/045/GCF_000146045.2_R64/GCF_000146045.2_R64_genomic.gff.gz&gt;)
    - essentials_file:  Essentials genes annotated from yeast , written using the systematic name standard , all in one column
    - gene_names_file:  This documents lists all the Saccharomyces cerevisiae S288c entries present in
</code></pre>
<p>this release of UniProtKB/Swiss-Prot.
Yeast (Saccharomyces cerevisiae): entries, gene names and cross-references to SGD.
Release:
2021_01 of 10-Feb-2021</p>
<pre><code>Outputs:
    gene_coordinates : a dict specifying for each gene the chromosome number the gene
    belongs to, the start gene coordinate, the end gene coordinate and the strand direction ('+' or '-'). 
    essential_coordinates: a dict specifying for each annotated essential gene the chromosome number the gene
    belongs to, the start gene coordinate, the end gene coordinate and the strand direction ('+' or '-'). 
    aliases_designation: a dict that for each systematic gene name specify the standard gene name.
</code></pre></div>
<details class="source">
<summary>
<span>Expand source code</span>
</summary>
<pre><code class="python">def read_genes(gff_file, essentials_file, gene_names_file):
    &#34;&#34;&#34;
    This function reads the useful information inside the gff_file, essentials_file and
    gene_names_file. 
    For the gff_file and essentials_file extracts the gene coordinates , specifying the chromosome, start ,end 
    and direction. 
    For the gene_names_files it translates the systematic name into the standard name.
    
    Usage: 

     [gene_coordinates, essential_coordinates, aliases_designation] = 
            read_genes(gff_file, essentials_file, gene_names_file)
    
    Inputs:
        - gff_file : Annotated genome from Saccharomyces cerevisiae (baker&#39;s yeast) (https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/146/045/GCF_000146045.2_R64/GCF_000146045.2_R64_genomic.gff.gz)
        - essentials_file:  Essentials genes annotated from yeast , written using the systematic name standard , all in one column
        - gene_names_file:  This documents lists all the Saccharomyces cerevisiae S288c entries present in
this release of UniProtKB/Swiss-Prot. 
            Yeast (Saccharomyces cerevisiae): entries, gene names and cross-references to SGD. 
             Release:     2021_01 of 10-Feb-2021
            
    Outputs:
        gene_coordinates : a dict specifying for each gene the chromosome number the gene
        belongs to, the start gene coordinate, the end gene coordinate and the strand direction (&#39;+&#39; or &#39;-&#39;). 
        essential_coordinates: a dict specifying for each annotated essential gene the chromosome number the gene
        belongs to, the start gene coordinate, the end gene coordinate and the strand direction (&#39;+&#39; or &#39;-&#39;). 
        aliases_designation: a dict that for each systematic gene name specify the standard gene name.  

    &#34;&#34;&#34;

    # Get gene position
    gene_coordinates = gene_position(gff_file)  #&#39;YAL069W&#39; | [&#39;I&#39;, 335, 649], ...

    # Get all annotated essential genes
    essential_coordinates = {}
    with open(essentials_file, &#34;r&#34;) as f:
        genes = f.readlines()[1:]
        for gene in genes:
            name = gene.strip(&#34;\n&#34;)
            essential_coordinates[name] = gene_coordinates.get(name).copy()

    # Get aliases of all genes
    aliases_designation = gene_aliases(gene_names_file)[0]  #&#39;YMR056C&#39; \ [&#39;AAC1&#39;], ...

    return gene_coordinates, essential_coordinates, aliases_designation</code></pre>
</details>
</dd>
</dl>
</section>
<section>
</section>
</article>
<nav id="sidebar">
<h1>Index</h1>
<div class="toc">
<ul></ul>
</div>
<ul id="index">
<li><h3>Super-module</h3>
<ul>
<li><code><a title="transposonmapper" href="../index.html">transposonmapper</a></code></li>
</ul>
</li>
<li><h3><a href="#header-submodules">Sub-modules</a></h3>
<ul>
<li><code><a title="transposonmapper.importing.verify_data_files" href="verify_data_files.html">transposonmapper.importing.verify_data_files</a></code></li>
</ul>
</li>
<li><h3><a href="#header-functions">Functions</a></h3>
<ul class="">
<li><code><a title="transposonmapper.importing.load_default_files" href="#transposonmapper.importing.load_default_files">load_default_files</a></code></li>
<li><code><a title="transposonmapper.importing.load_sgd_tab" href="#transposonmapper.importing.load_sgd_tab">load_sgd_tab</a></code></li>
<li><code><a title="transposonmapper.importing.read_genes" href="#transposonmapper.importing.read_genes">read_genes</a></code></li>
</ul>
</li>
</ul>
</nav>
</main>
<footer id="footer">
<p>Generated by <a href="https://pdoc3.github.io/pdoc" title="pdoc: Python API documentation generator"><cite>pdoc</cite> 0.10.0</a>.</p>
</footer>
</body>
</html>