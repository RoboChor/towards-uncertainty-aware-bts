grammar RequirementSubset ;

reqt_body : (nasa) ('.')?
          ;

nasa : (scope) (reqt_condition)
          (component SHALL)
          response
        ;

scope : ( IN scope_mode ) (',')?
        ;

reqt_condition
        : regular_condition ;

regular_condition
       :   qualified_condition1
           (',')?
       ;

qualifier_word
	    :
            IF
        ;

qualified_condition1
        : qualifier_word pre_condition
        ;

scope_mode : mode_name;

pre_condition
	: bool_expr
	;

component
          : component_name
          ;

response : satisfaction;

satisfaction : SATISFY post_condition ;

component_name : MISSION ;

mode_name    : ID ;

post_condition : bool_expr ;

bool_expr :  ('!') bool_expr
          | bool_expr '&' bool_expr
          | bool_expr ('|'|XOR) bool_expr
          | '(' bool_expr ')'
          | numeric_expr RELATIONAL_OP numeric_expr
          |  ID ('(' ( (bool_expr | numeric_expr) (',' (bool_expr | numeric_expr))*)? ')')?
          | 'true'
          | 'false'
          ;

numeric_expr :
               numeric_expr '^' numeric_expr
             |  '-' numeric_expr
             | numeric_expr ('*' | '/' | MOD) numeric_expr
             | numeric_expr ('+' | '-') numeric_expr
             | NUMBER
             | ID ( '(' ( (bool_expr | numeric_expr) (',' (bool_expr | numeric_expr))*)? ')')?
             | '(' numeric_expr ')'
             ;

MISSION : M I S S I O N;
AND : A N D;
FALSE : F A L S E;
IF : I F;
MOD : M O D;
OR : O R;
SATISFY : S A T I S F Y;
SHALL : S H A L L;
XOR : X O R;

ID     :    ((('a'..'z'|'A'..'Z') ('a'..'z'|'A'..'Z'|'0'..'9'|'_'|'.'|'%')*)
	    | STRING ) ;

STRING: '"' (ESC|.)*? '"' ;

RELATIONAL_OP     : '<' | '<=' | '>' | '>=' | '=' | '!='    ;

NUMBER :
         '-'? INT '.' [0-9]+ EXP?
       | '-'? INT EXP
       | '-'? INT
       ;

fragment EXP :
         [Ee] [+\-]? INT ;

fragment INT : '0' | [1-9][0-9]* ;

fragment ESC : '\\"' | '\\\\' ; // \" or \\

fragment A : [aA];
fragment B : [bB];
fragment C : [cC];
fragment D : [dD];
fragment E : [eE];
fragment F : [fF];
fragment G : [gG];
fragment H : [hH];
fragment I : [iI];
fragment J : [jJ];
fragment K : [kK];
fragment L : [lL];
fragment M : [mM];
fragment N : [nN];
fragment O : [oO];
fragment P : [pP];
fragment Q : [qQ];
fragment R : [rR];
fragment S : [sS];
fragment T : [tT];
fragment U : [uU];
fragment V : [vV];
fragment W : [wW];
fragment X : [xX];
fragment Y : [yY];
fragment Z : [zZ];