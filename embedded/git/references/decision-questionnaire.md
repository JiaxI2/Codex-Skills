# Decision Questionnaire

Resolve from repository evidence first. Ask the user only when a missing answer materially changes the result.

## A. Repository and audience

1. Is the repository public, private, customer-facing, or internal?
2. Who reads the README: developers, testers, customers, integrators, operators?
3. Is the repository an application, firmware product, reusable library, BSP, SDK, or delivery archive?
4. Is one README language sufficient, or are separate Chinese/English files needed?
5. Is the repository URL stable and known?

## B. Branch and delivery

1. Does `main/master` represent production, integration, or merely the default branch?
2. Are `develop/dev`, `test`, or `release` real deployment environments?
3. Must selected features be promoted independently?
4. Are multiple released versions maintained?
5. Must release and hotfix changes be back-merged?

## C. README

1. Which sections are necessary for the target reader?
2. Which details should live in docs rather than the README?
3. Which internal relative links are required?
4. Which external URLs are authoritative?
5. Are badges useful, accurate, and maintained?
6. Does the README need stable/latest release links or direct asset links?
7. Does the repository need a generated table of contents?

## D. CHANGELOG

1. Who consumes it?
2. Should entries be written per change, per PR fragment, or only at release?
3. Are PR/Issue links required?
4. Which categories make sense?
5. Does the project need compare URLs?
6. Is generated content acceptable as a draft?

## E. Version and Tag

1. Is SemVer appropriate?
2. Is the tag prefix `v`, another prefix, or none?
3. Must tags be annotated or signed?
4. What branch may receive official tags?
5. Are RC, beta, customer, or test-baseline tags needed?
6. Is a tag a formal immutable release or only an internal marker?

## F. Release Notes

1. Is this patch, minor, major, prerelease, customer delivery, or test baseline?
2. Are deprecations possible?
3. Are there breaking changes or migrations?
4. Is compatibility data required?
5. Are firmware assets published?
6. Are checksums required?
7. Must New Contributors be listed?
8. Is a separate full release document available?
9. Are releases immutable after publication?
10. Which language should GitHub Release notes use: Chinese, English, or bilingual?

## G. Firmware artifacts

1. Are binaries stored in Git, Git LFS, GitHub Release, or external storage?
2. Is a `firmware/` directory needed?
3. Which products, targets, and hardware revisions exist?
4. What naming scheme is required?
5. What build and validation metadata must be retained?
6. Are any signing materials secret?

## H. Automation

1. Should GitHub-generated release notes be enabled?
2. Are PR labels reliable enough for categories?
3. Should templates be rendered from configuration?
4. Should CI validate Markdown links and release headings?
5. Which actions remain manual approvals?
