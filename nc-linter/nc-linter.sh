#!/bin/bash
#
# nc-linter (Version 12): Report and rectify Numerical Control files.
# this version of nc-linter utilizes awk

TS="$( date '+%Y%m%d.%H%M%S' )"

BASE="/home/paul/SandBox/ncLinter"
DATA="./Inputs"
WORK="./Latest"
LOGS="./Logs"

#### Check and update numerical control data files.

function ncCheck {		#:: (void) < stdin: Params and Filenames.

	local AWK='''
BEGIN { Begin( ); }
	#..... Public Array Usage: used for each file in turn.
	#.. A: Insert After corresponding C row.
	#.. B: Insert Before corresponding C row.
	#.. C: Change area -- multiple edits can apply.
	#.. D: Delete (do not write) corresponding C row.
	#.. E: Events logged for corresponding C row.
	#.. F: File (original) data, set first time the C row is changed.
	#.. G: Global Statistics.
	#.. A, B and F can be multiline, using US as line separator.
function Begin( ) {
	RS = "(\015)?(\n)"; TSS = "%";
	NIL = ""; BLK = " "; SEP = "/"; US = "\037";
	G["Written logs"]; G["Written files"];
	#.. Patterns for various NC objects.
	reWS = "[\040\011]+"; reOWS = "[\040\011]*"; reBlank = "^" reOWS "$";
	reComment = "[(][^)]*[)]";
	reSerial = "^O[0-9]+";
	reDecExcess = "[-]?[0-9]*[.][0-9][0-9][0-9][0-9][0-9]+";
	reDecNumber = "[0-9.]+";
	reDecDouble = "[.].*[.]";
	reAddress = "[/]?[A-Z][-]?[0-9.]+";
	reWords = "^("reAddress"[\040\011]*)+";
}
###
### SECTION controls the complete process for a single NC File.
###
#.. Load up one file, fix it up, and save if any changes were made.
function Process (fn, Local, g, fnr, fnOutx, fnLogx) {
	#.. Clear all the global arrays.
	delete A; delete B; delete C; delete D; delete E; delete F;
	#.. Make output file names to match input.
	fnOut = fn ".new"; sub ("^.*[/]", dirWork SEP, fnOut);
	fnLog = fn ".log"; sub ("^.*[/]", dirLogs SEP, fnLog);
	#.. Load the file up.
	Append( E, 0, sprintf ("#### Logging run at %s", tStamp));
	Append( E, 0, sprintf ("#### %s", fn));

	if (! Reader( fn)) {
		Append( E, 0, "#### FAILED TO READ");
		Logger( "\n", fnLog);
		return;
	}
	#.. Apply all the tests and corrections.
	fixWhiteSpace( );
	fixComments( );
	fixGapAddress( );
	fixProgram( );
	fixDecExcess( );
	fixDecDouble( );
	fixTssMarks( );
	fixBadWords( );

	#.. If any changes, write out the corrected NC file.
	if (E["Fix"] > 0) {
		G["Fixes in " fn] = E["Fix"];
		Writer( "\r\n", fnOut);
	}
	#.. Write out the Events Log file.
	Logger( "\n", fnLog);
}
###
### SECTION contains all the file reading and writing functions.
###
#.. Load up a file into the C array.
function Reader (fn, Local, g, fnr) {
	while ((g = (getline < fn)) > 0) C[++fnr] = $0;
	if (g < 0) ++G["Error: " ERRNO " reading " fn];
	close (fn);
	++G["Files read"];
	if (! 787) G["Lines read from " fn] = fnr;
	return (g == 0 && fnr > 0);
}
#.. Write a new file with edits, inserts and deletes.
function Writer (nl, fn, Local, j) {
	for (j = 1; j in C; j++) {
		if (j in B) MultiLine( NIL, B[j], nl, fn);
		if (! (j in D)) printf ("%s%s", C[j], nl) > fn;
		if (j in A) MultiLine( NIL, A[j], nl, fn);
	}
	close (fn); ++G["Written files"];
}
#.. Write a log file with audit messages.
function Logger (nl, fn, Local, j) {
	if (0 in E) MultiLine( NIL, E[0], nl, fn);
	for (j = 1; j in C; j++) {
		if (j in E) MultiLine( NIL, E[j], nl, fn);
		if (j in F) {
			printf ("Original: %s%s", F[j], nl) > fn;
			if (j in B) MultiLine( "Before:   ", B[j], nl, fn);
			if (j in D) printf ("Deleted:  %s%s", F[j], nl) > fn;
			else printf ("Revised:  %s%s", C[j], nl) > fn;
			if (j in A) MultiLine( "After:    ", A[j], nl, fn);
		}
	}
	close (fnLog); ++G["Written logs"];
}
#.. Write a MultiLine text: may be Before, After, or Event log text.
function MultiLine (tag, tx, nl, fn, Local, j, M) {
	split (tx, M, US);
	for (j = 1; j in M; j++) printf ("%s%s%s", tag, M[j], nl) > fn;
}
###
### SECTION contains access functions for all the global arrays.
### You should not update the arrays directly, to avoid errors.
###
#.. Post Events for Global actions before all other events.
function Global (n, msg) {
	Append( E, 0, sprintf (".... Global fixes (%d) for %s", n, msg));
}
#.. Fix a line without triggering detailed reporting.
function Repair (j, txt) {
	C[j] = txt; ++E["Fix"];
}
#.. Add a MultiLine entry into B, A, or E array for a line.
function Append (X, j, msg) {
	if (! (j in X)) X[j] = msg; else X[j] = X[j] US msg;
}
#.. Post a reason for editing the line.
function Reason (j, msg) {
	if (msg != NIL) {
		if (! (j in E)) Append( E, j, sprintf ("\n.... Edits to line %d:", j));
		Append( E, j, "Reason:   " msg);
	}
}
#.. Change a line, post a reason, save the original for reporting.
function Change (j, txt, msg) {
	if (! (j in F)) F[j] = C[j];
	Repair( j, txt);
	Reason( j, msg);
}
#.. Mark a line for deletion, post a reason, save the original for reporting.
function Delete (j, msg) {
	if (! (j in F)) F[j] = C[j];
	D[j] = NIL; ++E["Fix"];
	Reason( j, msg);
}
###
### SECTION contains all the separate editing functions.
###
#.. Remove all leading and trailing white space, no detail reporting.
function fixWhiteSpace (Local, j, tx, nL, nR, tL, tR) {
	for (j = 1; j in C; ++j) {
		tx = C[j];
		nL = sub ("^" reWS, NIL, tx); tL += nL;
		nR = sub (reWS "$", NIL, tx); tR += nR;
		if (nL + nR > 0) Repair( j, tx);
	}
	if (tL > 0) Global( tL, "Leading Spaces");
	if (tR > 0) Global( tR, "Trailing Spaces");
}
#.. Fix bad comments: unbalanced or nested brackets.
function fixComments (Local, j, tx, nL, nR) {
	for (j = 1; j in C; ++j) {
		tx = fixCommentLine( C[j]);
		if (tx != NIL) Change( j, tx, "Invalid Comment");
	}
}
#.. Special to deal with comments we make ourselves.
function fixComment (tx, Local, tr) {
	tr = fixCommentLine( tx);
	return ((tr != NULL) ? tr : tx);
}
#.. Fix a comment on a line that may also have genuine code.
#.. NB. If no change was necessary, this returns NIL.
function fixCommentLine (tx, Local, br, nL, nR, tw, tn) {
	#.. Isolate the Brackets.
	br = tx; gsub (/[^()]/, NIL, br);
	#.. Count all variations of bracketing.
	++G["Brackets :" br ":"];
	#.. Simple or paired brackets need no action.
	if (br ~ /^([(][)])*$/) return (NIL);

	#.. Separate NC words from comments.
	if (match (tx, reWords)) {
		tw = substr (tx, RSTART, RLENGTH);
		tx = substr (tx, RSTART + RLENGTH);
	}
	#.. Fix up )..( brackets.
	sub (/^[)]+/, "(", tx); sub (/[(]+$/, ")", tx);
	#.. Count left and right brackets.
	nL = gsub (/[(]/, "(", tx); nR = gsub (/[)]/, ")", tx);
	#.. Unbalanced brackets fix: add more until balanced.
	while (nL < nR) { ++nL; tx = "(" tx; }
	while (nL > nR) { ++nR; tx = tx ")"; }
	#.. Isolate the changed brackets.
	br = tx; gsub (/[^()]/, NIL, br);
	#.. Nested Comment fix. Preserve the outermost brackets.
	if (br ~ /[(][(]|[)][)]/) {
		if (match (tx, /[(].*[)]/)) {
			#.. Make internal brackets into [..].
			tn = substr (tx, RSTART + 1, RLENGTH - 2);
			gsub (/[(]/, "[", tn); gsub (/[)]/, "]", tn);
			tx = substr (tx, 1, RSTART) tn substr (tx, RSTART+RLENGTH-1);
		}
	}
	return (tw tx);
}
#.. Separate run-together NC Words 
function fixGapAddress (Local, j, k, tx, v, c, nr) {
	for (j = 1; j in C; ++j) {
		v = NIL; c = NIL; tx = C[j];
		#.. Find the whitespace before any comment.
		k = match (tx, /[\040\011]*[(]/);
		#.. Save the comment separately.
		if (k) { c = substr (tx, k); tx = substr (tx, 1, k - 1); }
		#.. If no repeated Words, next line.
		if (tx !~ reAddress reAddress) continue;
		#.. Append a space to each address.
		while (match (tx, reAddress)) {
			v = v substr (tx, RSTART, RLENGTH) BLK;
			tx = substr (tx, RSTART + RLENGTH);
		}
		#.. Reconstruct the line.
		++nr; sub (reOWS "$", NIL, v); tx = v c;
		Repair( j, tx);
	}
	if (nr > 0) Global( nr, "Addresses Separated");
}
#.. Make initial Word starting with : into an O (Program name).
function fixProgram (Local, j, tx) {
	for (j = 1; j in C; ++j) {
		if (C[j] ~ /^[:][0-9]+( |$)/) {
			tx = C[j]; sub (/[:]/, "O", tx);
			Change( j, tx, "Repair Program address");
		}
	}
}
#.. Report (but cannot fix) invalid Address words.
function fixBadWords (Local, j, tx, k) {
	for (j = 1; j in C; ++j) {
		if (C[j] == TSS) continue;
		#.. Get the line, without any comments.
		k = index (C[j], "(");
		tx = (k == 0) ? C[j] : substr (C[j], 1, k-1);
		#.. Remove all valid addresses.
		while (match (tx, reAddress)) {
			#.. Get Stats on Address letters used.
			if (substr (tx, RSTART, 1) == "/")
			     ++G["Address type: " substr (tx, RSTART, 2)];
			else ++G["Address type: " substr (tx, RSTART, 1)];
			sub (reAddress, NIL, tx);
		}
		#.. Anything left consists of invalid Words.
		if (tx !~ reBlank) {
			gsub (/[\040\011]+/, BLK, tx);
			++G[sprintf ("Invalid Address %s", tx)];
			#.. CAUTION: Comment out the whole line.
			tx = fixComment( "( [Invalid Address: " tx "] " C[j] " )");
			Change( j, tx, "Invalid Address found");
		}
	}
}
#.. Make the TSS conformant.
function fixTssMarks (Local, j, k, p, e, tx) {
	#.. Make e the highest line number in the data.
	for (j = 1; j in C; ++j) e = j;
	#.. If first line is no TSS, insert one before it.
	if (C[1] != TSS) {
		Append( B, 1, TSS);
		Change( 1, C[1], "Insert initial TSS");
	}
	#.. Count back from e, so k is a valid TSS,
	#.. or the line containing the last NC Word in the file.
	for (k = e; k > p; --k) {
		if (C[k] == TSS) break;
		#.. If stop at a NC Word, add a TSS after it.
		if (C[k] ~ "^" reAddress) {
			Change( k, C[k], "Insert final TSS");
			Append( A, k, TSS);
			break;
		}
	}
	#.. Discard every TSS between those lines.
	for (j = 2; j < k; ++j) {
		if (C[j] == TSS) {
			Delete( j, "Delete Spurious TSS");
		}
		#.. CAUTION: Any other TSS within code words gets
		#.. the whole line commented out.
		if (C[j] != TSS && C[j] ~ "^[^(]*" TSS) {
			tx = fixComment( "( " C[j] " )");
			Change( j, tx, "Comment out spurious TSS");
		}
	}
	#.. For consistency, convert all non-blank trailing texts to comments.
	for (j = 1 + k; j <= e; ++j) {
		if (isEmpty( C[j])) continue;
		tx = fixComment( "( " C[j] " )");
		Change( j, tx, "Comment trailing text");
	}
}
#.. Enforce no more than 4-digit decimal accuracy.
function fixDecExcess (Local, j, n, s, tx, u, v) {
	for (j = 1; j in C; ++j) {
		n = 0; s = C[j];
		#.. Find the full number, like -62.76543
		while (match (s, reDecExcess)) {
			++n; v = substr (s, RSTART, RLENGTH);
			#.. Stats for variations.
			++G["DecExcess " v];
			#.. Reformat the number to round it off.
			tx = substr (s, 1, RSTART-1) sprintf ("%.4f", v);
			s = substr (s, RSTART+RLENGTH);
		}
		#.. Fix the line if anything changed.
		if (n) Change( j, tx s, "Excess digits");
	}
}
#.. Fix lines with numbers having multiple decimal points.
function fixDecDouble (Local, j, n, s, tx, u, v) {
	for (j = 1; j in C; ++j) {
		n = 0; tx = NIL; s = C[j];
		#.. Find any string of digits and dots.
		while (match (s, reDecNumber)) {
			v = substr (s, RSTART, RLENGTH);
			#.. Check if it contains two dots.
			if (v ~ reDecDouble) {
				#.. Remove all initial dots.
				++n; u = v; sub (/^[.]+/, NIL, v);
				#.. Hide the first dot, remove the rest, unhide the first.
				sub (/[.]/, "X", v); gsub (/[.]/, NIL, v); sub (/X/, ".", v);
				#.. Stats for variations of the problem.
				++G["DecDoubleFix |" u "| as |" v "|"];
			}
			tx = tx substr (s, 1, RSTART-1) v;
			s = substr (s, RSTART+RLENGTH);
		}
		#.. Update the line if anything changed.
		if (n) Change( j, tx s, "Double Decimal");
	}
}
#.. This checks for lines that are only whitespace and comments.
function isEmpty (tx) {
	gsub (reComment, NIL, tx); gsub (reBlank, NIL, tx);
	return (tx == NIL);
}
###
### SECTION Stores all the input stream: Parameters and File Names.
###
/^TIME=/ { ++G[BLK $0]; tStamp  = substr ($0, 6); next; }
/^DATA=/ { ++G[BLK $0]; dirData = substr ($0, 6); next; }
/^WORK=/ { ++G[BLK $0]; dirWork = substr ($0, 6); next; }
/^LOGS=/ { ++G[BLK $0]; dirLogs = substr ($0, 6); next; }
{ sub (/^[.][/]/, NIL); htFile[++htFile[0]] = $0; }
###
### SECTION Processes all the filenames from input.
###
function End (Local, fmtStats, Key, k) {
	for (j = 1; j in htFile; ++j) Process( dirData SEP htFile[j]);
	fmtStats = "%8d %s\n";
	asorti (G, Key);
	printf ("\nStatistics and Errors:\n");
	for (k = 1; k in Key; ++k) {
		printf (fmtStats, G[Key[k]], Key[k]);
	}
}
END { End( ); }
'''
	awk "${AWK}" "${FN}"
}

#### Script Body Starts Here.

	{
		echo "TIME=${TS}"
		echo "DATA=${DATA}"
		echo "WORK=${WORK}"
		echo "LOGS=${LOGS}"
		( cd "${DATA}" && find . -type f -size +0 -name '*.NC' )
	} | ncCheck > "${LOGS}/Stats.log" 2>&1

