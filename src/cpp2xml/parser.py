"""C++ header file parser using libclang."""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import cast

import clang.cindex
from clang.cindex import CursorKind


@dataclass
class Parameter:
    """Represents a function/method parameter."""
    name: str | None
    type_name: str
    is_anonymous: bool = False
    anonymous_id: str | None = None
    default_value: str | None = None  # Default parameter value if specified


@dataclass
class Function:
    """Represents a function declaration."""
    name: str
    return_type: str
    parameters: list[Parameter]
    is_method: bool = False
    is_static: bool = False
    is_const: bool = False
    is_volatile: bool = False
    is_virtual: bool = False
    access_specifier: str | None = None  # public, private, protected
    namespace: str | None = None
    location: str | None = None


@dataclass
class Field:
    """Represents a struct/class field."""
    name: str
    type_name: str
    access_specifier: str | None = None
    is_static: bool = False
    is_mutable: bool = False
    is_const: bool = False
    is_volatile: bool = False


@dataclass
class Struct:
    """Represents a struct declaration."""
    name: str
    fields: list[Field] = field(default_factory=list)
    methods: list[Function] = field(default_factory=list)
    operators: list['Operator'] = field(default_factory=list)
    nested_classes: list['Class'] = field(default_factory=list)
    nested_structs: list['Struct'] = field(default_factory=list)
    nested_enums: list['Enum'] = field(default_factory=list)
    friends: list['Friend'] = field(default_factory=list)
    namespace: str | None = None
    location: str | None = None


@dataclass
class Class:
    """Represents a class declaration."""
    name: str
    fields: list[Field] = field(default_factory=list)
    methods: list[Function] = field(default_factory=list)
    operators: list['Operator'] = field(default_factory=list)
    base_classes: list[str] = field(default_factory=list)
    nested_classes: list['Class'] = field(default_factory=list)
    nested_structs: list['Struct'] = field(default_factory=list)
    nested_enums: list['Enum'] = field(default_factory=list)
    friends: list['Friend'] = field(default_factory=list)
    namespace: str | None = None
    location: str | None = None


@dataclass
class Template:
    """Represents a template declaration."""
    name: str
    kind: str  # class, function, struct
    template_parameters: list[str] = field(default_factory=list)
    is_variadic: bool = False  # True if template uses parameter pack
    parameters: list[Parameter] = field(default_factory=list)  # For function templates
    return_type: str | None = None  # For function templates
    namespace: str | None = None
    location: str | None = None


@dataclass
class EnumValue:
    """Represents an enum value."""
    name: str
    value: int | None = None  # Explicit value if specified


@dataclass
class Enum:
    """Represents an enum declaration."""
    name: str
    values: list[EnumValue] = field(default_factory=list)
    is_scoped: bool = False  # True for enum class
    underlying_type: str | None = None  # For enum class with explicit type
    namespace: str | None = None
    location: str | None = None


@dataclass
class Union:
    """Represents a union declaration."""
    name: str
    fields: list[Field] = field(default_factory=list)
    methods: list[Function] = field(default_factory=list)
    namespace: str | None = None
    location: str | None = None


@dataclass
class Operator:
    """Represents an operator overload."""
    operator_kind: str  # e.g., "+", "==", "[]", "()", etc.
    return_type: str
    parameters: list[Parameter]
    is_member: bool = False
    access_specifier: str | None = None
    is_const: bool = False
    is_volatile: bool = False
    namespace: str | None = None
    location: str | None = None


@dataclass
class Friend:
    """Represents a friend declaration."""
    friend_type: str  # "function" or "class"
    name: str
    location: str | None = None


@dataclass
class ParsedHeader:
    """Represents the parsed content of a header file."""
    file_path: str
    relative_path: str
    base_path: str | None = None
    functions: list[Function] = field(default_factory=list)
    structs: list[Struct] = field(default_factory=list)
    classes: list[Class] = field(default_factory=list)
    templates: list[Template] = field(default_factory=list)
    enums: list[Enum] = field(default_factory=list)
    unions: list[Union] = field(default_factory=list)
    operators: list[Operator] = field(default_factory=list)


class CppParser:
    """Parser for C++ header files using libclang."""

    def __init__(self, include_paths: dict[str, str], clang_args: list[str] | None = None):
        """
        Initialize the parser.

        Args:
            include_paths: List of include directories to search
            clang_args: Additional arguments to pass to clang
        """
        self.include_paths = {Path(p).resolve(): mod for p, mod in include_paths.items()}
        self.clang_args = clang_args or []
        self.index = clang.cindex.Index.create()
        self._anonymous_counter = 0

    def _get_access_specifier(self, cursor) -> str | None:
        """Get the access specifier for a cursor."""
        access = cursor.access_specifier
        if access == clang.cindex.AccessSpecifier.PUBLIC:
            return "public"
        elif access == clang.cindex.AccessSpecifier.PRIVATE:
            return "private"
        elif access == clang.cindex.AccessSpecifier.PROTECTED:
            return "protected"
        return None

    def _get_namespace(self, cursor) -> str | None:
        """Get the namespace(s) containing this cursor."""
        namespaces = []
        parent = cursor.semantic_parent

        while parent is not None and parent.kind != CursorKind.TRANSLATION_UNIT:
            if parent.kind == CursorKind.NAMESPACE:
                namespaces.append(parent.spelling)
            parent = parent.semantic_parent

        if namespaces:
            # Reverse to get outermost to innermost order
            return "::".join(reversed(namespaces))
        return None

    def _is_in_target_file(self, cursor, target_file: str) -> bool:
        """Check if cursor is defined in the target file (not in includes)."""
        if cursor.location.file is None:
            return False
        cursor_file = str(cursor.location.file)
        return os.path.samefile(cursor_file, target_file)

    def _get_type_name(self, type_obj) -> str:
        """Get a readable type name from a clang type object."""
        return type_obj.spelling

    def _is_mutable_field(self, cursor) -> bool:
        """Check if a field is mutable."""
        return cursor.is_mutable_field() if hasattr(cursor, 'is_mutable_field') else False

    def _is_const_qualified(self, type_obj) -> bool:
        """Check if a type is const-qualified."""
        return type_obj.is_const_qualified()

    def _is_volatile_qualified(self, type_obj) -> bool:
        """Check if a type is volatile-qualified."""
        return type_obj.is_volatile_qualified()

    def _is_volatile_method(self, cursor) -> bool:
        """Check if a method is volatile-qualified."""
        # Check if 'volatile' appears in the method type spelling
        # (libclang doesn't provide a direct is_volatile_method() API)
        if hasattr(cursor, 'type'):
            type_str = cursor.type.spelling
            # Look for ' volatile' or 'const volatile' in function signature
            return ' volatile' in type_str
        return False

    def _get_default_value(self, cursor) -> str | None:
        """Extract default parameter value from cursor."""
        # Try to get default value from tokens
        tokens = list(cursor.get_tokens())
        if not tokens:
            return None

        # Look for '=' token and get everything after it
        found_equals = False
        default_tokens = []
        for token in tokens:
            if found_equals:
                # Stop at comma or closing paren
                if token.spelling in [',', ')']:
                    break
                default_tokens.append(token.spelling)
            elif token.spelling == '=':
                found_equals = True

        if default_tokens:
            return ' '.join(default_tokens)
        return None

    def _parse_parameters(self, cursor) -> list[Parameter]:
        """Parse function/method parameters."""
        parameters = []
        for arg in cursor.get_arguments():
            param_name = arg.spelling
            is_anonymous = not param_name or param_name == ""

            if is_anonymous:
                self._anonymous_counter += 1
                anonymous_id = f"__anon_param_{self._anonymous_counter}"
                param_name = anonymous_id
            else:
                anonymous_id = None

            # Get default value if present
            default_value = self._get_default_value(arg)

            param = Parameter(
                name=param_name,
                type_name=self._get_type_name(arg.type),
                is_anonymous=is_anonymous,
                anonymous_id=anonymous_id,
                default_value=default_value
            )
            parameters.append(param)

        return parameters

    def _parse_function(self, cursor, is_method: bool = False) -> Function:
        """Parse a function or method declaration."""
        return Function(
            name=cursor.spelling,
            return_type=self._get_type_name(cursor.result_type),
            parameters=self._parse_parameters(cursor),
            is_method=is_method,
            is_static=cursor.is_static_method() if is_method else False,
            is_const=cursor.is_const_method() if is_method else False,
            is_volatile=self._is_volatile_method(cursor) if is_method else False,
            is_virtual=cursor.is_virtual_method() if is_method else False,
            access_specifier=self._get_access_specifier(cursor) if is_method else None,
            namespace=self._get_namespace(cursor) if not is_method else None,
            location=f"{cursor.location.line}:{cursor.location.column}"
        )

    def _parse_field(self, cursor) -> Field:
        """Parse a struct/class field."""
        return Field(
            name=cursor.spelling,
            type_name=self._get_type_name(cursor.type),
            access_specifier=self._get_access_specifier(cursor),
            is_static=cursor.storage_class == clang.cindex.StorageClass.STATIC,
            is_mutable=self._is_mutable_field(cursor),
            is_const=self._is_const_qualified(cursor.type),
            is_volatile=self._is_volatile_qualified(cursor.type)
        )

    def _parse_struct_or_class(self, cursor, is_class: bool = False) -> Class | Struct:
        """Parse a struct or class declaration."""
        fields = []
        methods = []
        operators = []
        base_classes = []
        nested_classes: list[Class] = []
        nested_structs: list[Struct] = []
        nested_enums = []
        friends = []

        # Get base classes
        for child in cursor.get_children():
            if child.kind == CursorKind.CXX_BASE_SPECIFIER:
                base_classes.append(child.type.spelling)

        # Parse members
        for child in cursor.get_children():
            if not self._is_in_target_file(child, cursor.location.file.name):
                continue

            if child.kind == CursorKind.FIELD_DECL:
                fields.append(self._parse_field(child))
            elif child.kind == CursorKind.VAR_DECL:
                # Static fields appear as VAR_DECL in the AST
                fields.append(self._parse_field(child))
            elif child.kind in (CursorKind.CXX_METHOD, CursorKind.CONSTRUCTOR, CursorKind.DESTRUCTOR):
                # Check if this is an operator overload
                if child.spelling.startswith("operator"):
                    operator = self._parse_operator(child)
                    if operator:
                        operators.append(operator)
                else:
                    methods.append(self._parse_function(child, is_method=True))
            elif child.kind == CursorKind.CLASS_DECL and child.is_definition():
                nested_classes.append(cast(Class, self._parse_struct_or_class(child, is_class=True)))
            elif child.kind == CursorKind.STRUCT_DECL and child.is_definition():
                nested_structs.append(cast(Struct, self._parse_struct_or_class(child, is_class=False)))
            elif child.kind == CursorKind.ENUM_DECL:
                nested_enums.append(self._parse_enum(child))
            elif child.kind == CursorKind.FRIEND_DECL:
                friend = self._parse_friend(child)
                if friend:
                    friends.append(friend)

        if is_class:
            return Class(
                name=cursor.spelling,
                fields=fields,
                methods=methods,
                operators=operators,
                base_classes=base_classes,
                nested_classes=nested_classes,
                nested_structs=nested_structs,
                nested_enums=nested_enums,
                friends=friends,
                namespace=self._get_namespace(cursor),
                location=f"{cursor.location.line}:{cursor.location.column}"
            )
        else:
            return Struct(
                name=cursor.spelling,
                fields=fields,
                methods=methods,
                operators=operators,
                nested_classes=nested_classes,
                nested_structs=nested_structs,
                nested_enums=nested_enums,
                friends=friends,
                namespace=self._get_namespace(cursor),
                location=f"{cursor.location.line}:{cursor.location.column}"
            )

    def _get_template_parameters(self, cursor) -> tuple[list[str], bool]:
        """Extract template parameter names and check if variadic."""
        params = []
        is_variadic = False
        for child in cursor.get_children():
            if child.kind in (CursorKind.TEMPLATE_TYPE_PARAMETER,
                             CursorKind.TEMPLATE_NON_TYPE_PARAMETER,
                             CursorKind.TEMPLATE_TEMPLATE_PARAMETER):
                param_name = child.spelling or child.displayname
                # Check if this is a parameter pack (variadic)
                if child.kind == CursorKind.TEMPLATE_TYPE_PARAMETER:
                    # Check for "..." in the tokens
                    tokens = list(child.get_tokens())
                    for token in tokens:
                        if token.spelling == '...':
                            is_variadic = True
                            param_name = param_name + "..."
                            break
                params.append(param_name)
        return params, is_variadic

    def _parse_template(self, cursor) -> Template | None:
        """Parse a template declaration."""
        template_params, is_variadic = self._get_template_parameters(cursor)
        namespace = self._get_namespace(cursor)

        # For CLASS_TEMPLATE or FUNCTION_TEMPLATE, use the cursor itself
        # The template cursor represents the templated entity
        templated_entity = cursor

        if cursor.kind == CursorKind.CLASS_TEMPLATE:
            entity_kind = "class"
        elif cursor.kind == CursorKind.FUNCTION_TEMPLATE:
            entity_kind = "function"
        else:
            return None

        # Build template object based on entity kind
        if entity_kind in ("class", "struct"):
            return Template(
                name=templated_entity.spelling,
                kind=entity_kind,
                template_parameters=template_params,
                is_variadic=is_variadic,
                namespace=namespace,
                location=f"{cursor.location.line}:{cursor.location.column}"
            )
        elif entity_kind in ("function", "method"):
            # Try to parse parameters, but handle case where there are none
            try:
                params = self._parse_parameters(templated_entity) if templated_entity.kind != CursorKind.CLASS_TEMPLATE else []
                return_type = self._get_type_name(templated_entity.result_type) if hasattr(templated_entity, 'result_type') else None
            except:
                params = []
                return_type = None

            return Template(
                name=templated_entity.spelling,
                kind=entity_kind,
                template_parameters=template_params,
                is_variadic=is_variadic,
                parameters=params,
                return_type=return_type,
                namespace=namespace,
                location=f"{cursor.location.line}:{cursor.location.column}"
            )

        return None

    def _parse_enum(self, cursor) -> Enum:
        """Parse an enum declaration."""
        values = []
        for child in cursor.get_children():
            if child.kind == CursorKind.ENUM_CONSTANT_DECL:
                # Try to get the explicit value if available
                enum_value = None
                try:
                    enum_value = child.enum_value
                except:
                    pass
                values.append(EnumValue(name=child.spelling, value=enum_value))

        # Check if it's a scoped enum (enum class)
        is_scoped = cursor.is_scoped_enum() if hasattr(cursor, 'is_scoped_enum') else False

        # Get underlying type if specified
        underlying_type = None
        if cursor.enum_type and cursor.enum_type.spelling:
            underlying_type = cursor.enum_type.spelling

        return Enum(
            name=cursor.spelling,
            values=values,
            is_scoped=is_scoped,
            underlying_type=underlying_type,
            namespace=self._get_namespace(cursor),
            location=f"{cursor.location.line}:{cursor.location.column}"
        )

    def _parse_union(self, cursor) -> Union:
        """Parse a union declaration."""
        fields = []
        methods = []

        for child in cursor.get_children():
            if not self._is_in_target_file(child, cursor.location.file.name):
                continue

            if child.kind == CursorKind.FIELD_DECL:
                fields.append(self._parse_field(child))
            elif child.kind == CursorKind.VAR_DECL:
                # Static fields appear as VAR_DECL in the AST
                fields.append(self._parse_field(child))
            elif child.kind in (CursorKind.CXX_METHOD, CursorKind.CONSTRUCTOR, CursorKind.DESTRUCTOR):
                methods.append(self._parse_function(child, is_method=True))

        return Union(
            name=cursor.spelling,
            fields=fields,
            methods=methods,
            namespace=self._get_namespace(cursor),
            location=f"{cursor.location.line}:{cursor.location.column}"
        )

    def _parse_operator(self, cursor) -> Operator | None:
        """Parse an operator overload."""
        # Extract operator kind from the name
        name = cursor.spelling
        if not name.startswith("operator"):
            return None

        # Remove "operator" prefix and trim
        operator_kind = name[8:].strip()

        return Operator(
            operator_kind=operator_kind,
            return_type=self._get_type_name(cursor.result_type),
            parameters=self._parse_parameters(cursor),
            is_member=cursor.semantic_parent.kind in (CursorKind.CLASS_DECL, CursorKind.STRUCT_DECL),
            access_specifier=self._get_access_specifier(cursor),
            is_const=cursor.is_const_method() if hasattr(cursor, 'is_const_method') else False,
            is_volatile=self._is_volatile_method(cursor),
            namespace=self._get_namespace(cursor),
            location=f"{cursor.location.line}:{cursor.location.column}"
        )

    def _parse_friend(self, cursor) -> Friend | None:
        """Parse a friend declaration."""
        # Try to get the referenced entity
        for child in cursor.get_children():
            if child.kind == CursorKind.FUNCTION_DECL:
                return Friend(
                    friend_type="function",
                    name=child.spelling,
                    location=f"{cursor.location.line}:{cursor.location.column}"
                )
            elif child.kind in (CursorKind.CLASS_DECL, CursorKind.STRUCT_DECL):
                return Friend(
                    friend_type="class",
                    name=child.spelling,
                    location=f"{cursor.location.line}:{cursor.location.column}"
                )
            elif child.kind == CursorKind.TYPE_REF:
                # Friend class forward declaration
                return Friend(
                    friend_type="class",
                    name=child.spelling,
                    location=f"{cursor.location.line}:{cursor.location.column}"
                )

        return None

    def _traverse_cursor(self, cursor, target_file: str, result: ParsedHeader):
        """Recursively traverse the AST and extract declarations."""
        # Skip if not in target file, but allow TRANSLATION_UNIT to continue
        if cursor.kind != CursorKind.TRANSLATION_UNIT and not self._is_in_target_file(cursor, target_file):
            return

        if cursor.kind == CursorKind.FUNCTION_DECL:
            # Check if this is an operator overload
            if cursor.spelling.startswith("operator"):
                operator = self._parse_operator(cursor)
                if operator and not operator.is_member:
                    result.operators.append(operator)
            else:
                result.functions.append(self._parse_function(cursor))
        elif cursor.kind == CursorKind.STRUCT_DECL and cursor.is_definition():
            result.structs.append(cast(Struct, self._parse_struct_or_class(cursor, is_class=False)))
        elif cursor.kind == CursorKind.CLASS_DECL and cursor.is_definition():
            result.classes.append(cast(Class, self._parse_struct_or_class(cursor, is_class=True)))
        elif cursor.kind == CursorKind.UNION_DECL and cursor.is_definition():
            result.unions.append(self._parse_union(cursor))
        elif cursor.kind == CursorKind.ENUM_DECL:
            result.enums.append(self._parse_enum(cursor))
        elif cursor.kind == CursorKind.CLASS_TEMPLATE:
            template = self._parse_template(cursor)
            if template:
                result.templates.append(template)
            # Don't traverse children - they're already handled in _parse_template
            return
        elif cursor.kind == CursorKind.FUNCTION_TEMPLATE:
            template = self._parse_template(cursor)
            if template:
                result.templates.append(template)
            # Don't traverse children - they're already handled in _parse_template
            return

        # Continue traversing for nested declarations
        for child in cursor.get_children():
            self._traverse_cursor(child, target_file, result)

    def parse_header(self, header_path_str: str) -> ParsedHeader:
        """
        Parse a single header file.

        Args:
            header_path: Path to the header file

        Returns:
            ParsedHeader object containing the parsed elements
        """
        header_path = Path(header_path_str).resolve()

        # Determine relative path from include paths
        relative_path = None
        base_path = None
        for include_path in self.include_paths:
            try:
                relative_path = header_path.relative_to(include_path)
                base_path = include_path
                break
            except ValueError:
                continue

        if relative_path is None:
            relative_path = Path(header_path.name)

        # Build clang arguments
        args = [f"-I{path}" for path in self.include_paths] + self.clang_args
        args.extend(["-x", "c++", "-std=c++17"])

        # Parse the translation unit
        tu = self.index.parse(
            str(header_path),
            args=args,
            options=clang.cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD
        )

        # Check for errors
        for diag in tu.diagnostics:
            if diag.severity >= clang.cindex.Diagnostic.Error:
                print(f"Parse error in {header_path}: {diag.spelling}")

        # Create result object
        result = ParsedHeader(
            file_path=str(header_path),
            relative_path=str(relative_path),
            base_path=str(base_path) if base_path else None
        )

        # Reset anonymous counter for each file
        self._anonymous_counter = 0

        # Traverse the AST
        self._traverse_cursor(tu.cursor, str(header_path), result)

        return result

    def parse_all_headers(self) -> dict[str, list[ParsedHeader]]:
        """
        Parse all header files found in the include paths.

        Returns:
            List of ParsedHeader objects
        """
        results: dict[str, list[ParsedHeader]] = {}
        header_extensions = {".h", ".hpp", ".hxx", ".hh"}

        for include_path, mod in self.include_paths.items():
            for root, _, files in os.walk(include_path):
                for file in files:
                    if Path(file).suffix in header_extensions:
                        header_path = Path(root) / file
                        try:
                            parsed = self.parse_header(str(header_path))
                            results.setdefault(mod, []).append(parsed)
                        except Exception as e:
                            print(f"Error parsing {header_path}: {e}")

        return results
