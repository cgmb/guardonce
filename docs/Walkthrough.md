# Walkthrough
These are a couple of examples of converting projects back and forth between
include guards and #pragma once.

## Abseil
[Abseil][1] is a good example of a project that uses include guards. If we want
to check that it is consistently following its include guard naming convention,
we can supply a [pattern](PatternLanguage.md) to `checkguard`. Let's download
it and try. Just in case the project has changed since this guide was written,
we'll checkout the same version I used.

```bash
git clone https://github.com/abseil/abseil-cpp.git
cd abseil-cpp
git checkout cc4bed2d74f7c8717e31f9579214ab52a9c9c610
checkguard -r --only guard -p "path | upper | append _" absl
```

There should be nothing printed, indicating that every header has an include
guard matching the expected pattern. If you need to check that you constructed
your pattern correctly, adding `-n` will cause `checkguard` to print out the
expected guards rather than doing the check.

It's not strictly necessary to check your headers before converting, but it's
a good time to catch old mistakes. I recommend it. Checking usually doesn't
take very long. Doing the check also gives you the confidence to specify an
expected pattern for `guard2once` to look for when converting, like so:

```bash
guard2once -r -p "path | upper | append _" absl
```

A simple `guard2once -r absl` would have been sufficient, since `guard2once`
does a pretty good job of guessing which defines are include guards when no
pattern is specified, but it's nice to keep guesswork out of the process when
possible.

Converting back is fairly simple as well. `once2guard` takes the same arguments
as we passed to `guard2once`. Though, Abseil has a comment after the #endif, so
we'll need to supply a template to get the exact same #endif style.

```bash
once2guard -r -p "path | upper | append _" -s "#endif  // %\n" absl
```

Checking `git diff` should show that the round-trip from include guards
to #pragma once and back again resulted in no significant changes. The only
differences come from a few files that had mistakenly used a different #endif
style. Those headers were changed by `once2guard` to match the rest of the
project.

## Folly
The [Folly][2] project uses #pragma once exclusively. Let's convert their
project to use include guards. First, we'll download the project and check
their headers are all properly protected by #pragma once before converting.
It's simple enough to do that with a few commands.

```bash
git clone https://github.com/Facebook/folly.git
cd folly
git checkout 79869083465aabfcb9d9abd7f31ecfe812e3464b
checkguard -r --only once folly
```

However, `checkguard` complains about whole bunch of files:

```
folly/Format-inl.h
folly/AtomicHashMap-inl.h
folly/Singleton-inl.h
folly/Foreach-inl.h
folly/Random-inl.h
folly/Arena-inl.h
folly/AtomicHashArray-inl.h
folly/Uri-inl.h
folly/ExceptionWrapper-inl.h
folly/gen/Core-inl.h
folly/gen/Parallel-inl.h
folly/gen/String-inl.h
folly/gen/File-inl.h
folly/gen/ParallelMap-inl.h
folly/gen/Combine-inl.h
folly/gen/Base-inl.h
folly/experimental/hazptr/hazptr-impl.h
folly/experimental/symbolizer/Elf-inl.h
folly/test/FBStringTestBenchmarks.cpp.h
folly/test/FBVectorTestBenchmarks.cpp.h
folly/fibers/WhenN-inl.h
folly/fibers/Baton-inl.h
folly/fibers/Promise-inl.h
folly/fibers/EventBaseLoopController-inl.h
folly/fibers/AtomicBatchDispatcher-inl.h
folly/fibers/AddTasks-inl.h
folly/fibers/ForEach-inl.h
folly/io/RecordIO-inl.h
```

After looking through a few of these files, it appears that files ending in
`-inl.h`, `.cpp.h` and `-impl.h` are designed such that they don't need a
guard. We can add them to our exclude list.

```bash
checkguard -r --only once -e="*-inl.h" -e="*.cpp.h" -e="*-impl.h" folly
```

Now `checkguard` has no complaints. Great! Strictly speaking, we didn't really
need to check anything before converting, but we learned a little more about
this project's quirks. If there were any actual oversights, this would have
been a good time to address them.

Our next question is what sort of include guard we want. There's a lot of
different patterns out there and no real standard. To ensure uniqueness within
our repository, let's use the full path as the base, prefix the company
initials, and make it all uppercase to match our coding standard's naming
guidelines for macro names.

```bash
once2guard -r -p "path | prepend fb_ | upper" folly
```

If we take a look at the output of `git diff`, we can see that our headers now
all use include guards. For example, we if look at `folly/AtomicUnorderedMap.h`:

```patch
diff --git a/folly/AtomicUnorderedMap.h b/folly/AtomicUnorderedMap.h
index 21cf55e..767ae47 100644
--- a/folly/AtomicUnorderedMap.h
+++ b/folly/AtomicUnorderedMap.h
@@ -14,7 +14,8 @@
  * limitations under the License.
  */
 
-#pragma once
+#ifndef FB_FOLLY_ATOMICUNORDEREDMAP_H
+#define FB_FOLLY_ATOMICUNORDEREDMAP_H
 
 #include <atomic>
 #include <cstdint>
@@ -521,3 +522,4 @@ struct MutableData {
 
 
 }
+#endif
```

That pattern is a little hard to read, though. Not a big deal, but maybe a
slightly different pattern would be better. Let's throw away our changes and
try again, using `snake` to separate words in the filename.

```bash
git checkout .
once2guard -r -p "path | snake | prepend fb_ | upper" folly
```

Taking a look through our diff output again, I think the pattern is much
improved.

```patch
diff --git a/folly/AtomicUnorderedMap.h b/folly/AtomicUnorderedMap.h
index 21cf55e..24c310f 100644
--- a/folly/AtomicUnorderedMap.h
+++ b/folly/AtomicUnorderedMap.h
@@ -14,7 +14,8 @@
  * limitations under the License.
  */
 
-#pragma once
+#ifndef FB_FOLLY_ATOMIC_UNORDERED_MAP_H
+#define FB_FOLLY_ATOMIC_UNORDERED_MAP_H
 
 #include <atomic>
 #include <cstdint>
@@ -521,3 +522,4 @@ struct MutableData {
 
 
 }
+#endif
```

Of course, guardonce would be nothing if it couldn't make switching back easy.
Let's do it.

```bash
guard2once -r folly
```

Done. We probably should have specified our include guard pattern, especially
since we already knew it. But, if we check `git diff` we can see that this was
a perfect round-trip from #pragma once to include guards and back. Specifying
the expected pattern is a good, cautious thing to do and I recommend it whenever
possible, but the heuristics for identifying include guards without a pattern
usually get things right anyways.

## Disclaimer
I am not affiliated with either of the Abseil or Folly projects. They are
merely convenient examples.

[1]: https://github.com/abseil/abseil-cpp
[2]: https://github.com/Facebook/folly
