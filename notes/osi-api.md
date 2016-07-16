Title: The Open Source License API
Date: 2016-07-16 15:30
Tags: osi, opendata, licenses
Category: osi
Slug: osi-license-api
Author: Paul Tagliamonte
TwitterSite: @paultag
TwitterCreator: @paultag
TwitterImage: https://opensource.org/files/osi_keyhole_600X600_90ppi.png

Around a year ago, I started hacking together a machine readable version
of the OSI approved licenses list, and casually picking parts up until it
was ready to launch. A few weeks ago, we officially announced
the [osi license api](https://opensource.org/node/822), which is now
live at [api.opensource.org](https://api.opensource.org/).

I also took a whack at writing a few API bindings, in
[Python](https://github.com/opensourceorg/python-opensource),
[Ruby](https://github.com/opensourceorg/ruby-opensourceapi),
and using the models from the API implementation itself in
[Go](https://github.com/OpenSourceOrg/api/tree/master/client). In the following
few weeks, [Clint](https://github.com/clinty) wrote one in [Haskell](https://github.com/OpenSourceOrg/haskell-opensource),
[Eriol](https://mornie.org/) wrote one in [Rust](https://github.com/opensourceorg/rust-opensource),
and [Oliver](https://ironholds.org/) wrote one in [R](https://cran.r-project.org/web/packages/osi/).

The data is sourced from a [repo on GitHub](https://github.com/opensourceorg/licenses),
the `licenses` repo under `OpenSourceOrg`. Pull Requests against that repo are
wildly encouraged! Additional data ideas, cleanup or more hand collected data
would be wonderful!

In the meantime, use-cases for using this API range from language package
managers pulling OSI approval of a licence programatically to using a license
identifier as defined in one dataset (SPDX, for exampele), and using that
to find the identifer as it exists in another system (DEP5, Wikipedia,
TL;DR Legal).

Patches are hugly welcome, as are bug reports or ideas! I'd also love more
API wrappers for other languages!
