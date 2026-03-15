"""XML generator for parsed C++ headers."""

import os
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom

from .parser import (
    ParsedHeader, Function, Struct, Class, Template,
    Parameter, Field, Enum, Union, Operator, Friend
)


class XmlGenerator:
    """Generates XML documentation from parsed C++ headers."""

    def __init__(self, output_dir: str):
        """
        Initialize the XML generator.

        Args:
            output_dir: Directory where XML files will be written
        """
        self.output_dir = Path(output_dir)

    def _create_parameter_element(self, param: Parameter) -> ET.Element:
        """Create XML element for a parameter."""
        param_elem = ET.Element("parameter")
        param_elem.set("name", param.name or "")
        param_elem.set("type", param.type_name)

        if param.default_value:
            param_elem.set("default", param.default_value)

        if param.is_anonymous:
            param_elem.set("is_anonymous", "true")
            if param.anonymous_id:
                param_elem.set("anonymous_id", param.anonymous_id)

                # Create a type definition for anonymous parameter
                typedef_elem = ET.Element("type_definition")
                typedef_elem.set("id", param.anonymous_id)
                typedef_elem.set("underlying_type", param.type_name)
                param_elem.append(typedef_elem)

        return param_elem

    def _create_field_element(self, field: Field) -> ET.Element:
        """Create XML element for a struct/class field."""
        field_elem = ET.Element("field")
        field_elem.set("name", field.name)
        field_elem.set("type", field.type_name)

        if field.access_specifier:
            field_elem.set("access", field.access_specifier)
        if field.is_static:
            field_elem.set("static", "true")
        if field.is_mutable:
            field_elem.set("mutable", "true")
        if field.is_const:
            field_elem.set("const", "true")
        if field.is_volatile:
            field_elem.set("volatile", "true")

        return field_elem

    def _create_function_element(self, func: Function) -> ET.Element:
        """Create XML element for a function or method."""
        if func.is_method:
            func_elem = ET.Element("method")
            if func.access_specifier:
                func_elem.set("access", func.access_specifier)
            if func.is_static:
                func_elem.set("static", "true")
            if func.is_const:
                func_elem.set("const", "true")
            if func.is_volatile:
                func_elem.set("volatile", "true")
            if func.is_virtual:
                func_elem.set("virtual", "true")
        else:
            func_elem = ET.Element("function")

        func_elem.set("name", func.name)
        func_elem.set("return_type", func.return_type)

        if func.namespace:
            func_elem.set("namespace", func.namespace)

        if func.location:
            func_elem.set("location", func.location)

        # Add parameters
        if func.parameters:
            params_elem = ET.SubElement(func_elem, "parameters")
            for param in func.parameters:
                params_elem.append(self._create_parameter_element(param))

        return func_elem

    def _create_struct_element(self, struct: Struct) -> ET.Element:
        """Create XML element for a struct."""
        struct_elem = ET.Element("struct")
        struct_elem.set("name", struct.name)

        if struct.namespace:
            struct_elem.set("namespace", struct.namespace)

        if struct.location:
            struct_elem.set("location", struct.location)

        # Add fields
        if struct.fields:
            fields_elem = ET.SubElement(struct_elem, "fields")
            for field in struct.fields:
                fields_elem.append(self._create_field_element(field))

        # Add methods
        if struct.methods:
            methods_elem = ET.SubElement(struct_elem, "methods")
            for method in struct.methods:
                methods_elem.append(self._create_function_element(method))

        # Add operators
        if struct.operators:
            operators_elem = ET.SubElement(struct_elem, "operators")
            for operator in struct.operators:
                operators_elem.append(self._create_operator_element(operator))

        # Add nested classes
        if struct.nested_classes:
            nested_classes_elem = ET.SubElement(struct_elem, "nested_classes")
            for nested_class in struct.nested_classes:
                nested_classes_elem.append(self._create_class_element(nested_class))

        # Add nested structs
        if struct.nested_structs:
            nested_structs_elem = ET.SubElement(struct_elem, "nested_structs")
            for nested_struct in struct.nested_structs:
                nested_structs_elem.append(self._create_struct_element(nested_struct))

        # Add nested enums
        if struct.nested_enums:
            nested_enums_elem = ET.SubElement(struct_elem, "nested_enums")
            for nested_enum in struct.nested_enums:
                nested_enums_elem.append(self._create_enum_element(nested_enum))

        # Add friends
        if struct.friends:
            friends_elem = ET.SubElement(struct_elem, "friends")
            for friend in struct.friends:
                friends_elem.append(self._create_friend_element(friend))

        return struct_elem

    def _create_class_element(self, cls: Class) -> ET.Element:
        """Create XML element for a class."""
        class_elem = ET.Element("class")
        class_elem.set("name", cls.name)

        if cls.namespace:
            class_elem.set("namespace", cls.namespace)

        if cls.location:
            class_elem.set("location", cls.location)

        # Add base classes
        if cls.base_classes:
            bases_elem = ET.SubElement(class_elem, "base_classes")
            for base in cls.base_classes:
                base_elem = ET.SubElement(bases_elem, "base")
                base_elem.set("name", base)

        # Add fields
        if cls.fields:
            fields_elem = ET.SubElement(class_elem, "fields")
            for field in cls.fields:
                fields_elem.append(self._create_field_element(field))

        # Add methods
        if cls.methods:
            methods_elem = ET.SubElement(class_elem, "methods")
            for method in cls.methods:
                methods_elem.append(self._create_function_element(method))

        # Add operators
        if cls.operators:
            operators_elem = ET.SubElement(class_elem, "operators")
            for operator in cls.operators:
                operators_elem.append(self._create_operator_element(operator))

        # Add nested classes
        if cls.nested_classes:
            nested_classes_elem = ET.SubElement(class_elem, "nested_classes")
            for nested_class in cls.nested_classes:
                nested_classes_elem.append(self._create_class_element(nested_class))

        # Add nested structs
        if cls.nested_structs:
            nested_structs_elem = ET.SubElement(class_elem, "nested_structs")
            for nested_struct in cls.nested_structs:
                nested_structs_elem.append(self._create_struct_element(nested_struct))

        # Add nested enums
        if cls.nested_enums:
            nested_enums_elem = ET.SubElement(class_elem, "nested_enums")
            for nested_enum in cls.nested_enums:
                nested_enums_elem.append(self._create_enum_element(nested_enum))

        # Add friends
        if cls.friends:
            friends_elem = ET.SubElement(class_elem, "friends")
            for friend in cls.friends:
                friends_elem.append(self._create_friend_element(friend))

        return class_elem

    def _create_template_element(self, template: Template) -> ET.Element:
        """Create XML element for a template."""
        template_elem = ET.Element("template")
        template_elem.set("name", template.name)
        template_elem.set("kind", template.kind)

        if template.is_variadic:
            template_elem.set("variadic", "true")

        if template.namespace:
            template_elem.set("namespace", template.namespace)

        if template.location:
            template_elem.set("location", template.location)

        # Add template parameters
        if template.template_parameters:
            tparams_elem = ET.SubElement(template_elem, "template_parameters")
            for tparam in template.template_parameters:
                tp_elem = ET.SubElement(tparams_elem, "template_parameter")
                tp_elem.set("name", tparam)

        # Add function parameters if it's a function template
        if template.kind in ("function", "method") and template.parameters:
            params_elem = ET.SubElement(template_elem, "parameters")
            for param in template.parameters:
                params_elem.append(self._create_parameter_element(param))

        # Add return type if it's a function template
        if template.kind in ("function", "method") and template.return_type:
            template_elem.set("return_type", template.return_type)

        return template_elem

    def _create_enum_element(self, enum: Enum) -> ET.Element:
        """Create XML element for an enum."""
        enum_elem = ET.Element("enum_class" if enum.is_scoped else "enum")
        enum_elem.set("name", enum.name)

        if enum.namespace:
            enum_elem.set("namespace", enum.namespace)

        if enum.underlying_type:
            enum_elem.set("underlying_type", enum.underlying_type)

        if enum.location:
            enum_elem.set("location", enum.location)

        # Add enum values
        if enum.values:
            values_elem = ET.SubElement(enum_elem, "values")
            for val in enum.values:
                val_elem = ET.SubElement(values_elem, "value")
                val_elem.set("name", val.name)
                if val.value is not None:
                    val_elem.set("value", str(val.value))

        return enum_elem

    def _create_union_element(self, union: Union) -> ET.Element:
        """Create XML element for a union."""
        union_elem = ET.Element("union")
        union_elem.set("name", union.name)

        if union.namespace:
            union_elem.set("namespace", union.namespace)

        if union.location:
            union_elem.set("location", union.location)

        # Add fields
        if union.fields:
            fields_elem = ET.SubElement(union_elem, "fields")
            for field in union.fields:
                fields_elem.append(self._create_field_element(field))

        # Add methods
        if union.methods:
            methods_elem = ET.SubElement(union_elem, "methods")
            for method in union.methods:
                methods_elem.append(self._create_function_element(method))

        return union_elem

    def _create_operator_element(self, operator: Operator) -> ET.Element:
        """Create XML element for an operator overload."""
        op_elem = ET.Element("operator")
        op_elem.set("kind", operator.operator_kind)
        op_elem.set("return_type", operator.return_type)

        if operator.is_member:
            op_elem.set("member", "true")
            if operator.access_specifier:
                op_elem.set("access", operator.access_specifier)
            if operator.is_const:
                op_elem.set("const", "true")
            if operator.is_volatile:
                op_elem.set("volatile", "true")
        else:
            if operator.namespace:
                op_elem.set("namespace", operator.namespace)

        if operator.location:
            op_elem.set("location", operator.location)

        # Add parameters
        if operator.parameters:
            params_elem = ET.SubElement(op_elem, "parameters")
            for param in operator.parameters:
                params_elem.append(self._create_parameter_element(param))

        return op_elem

    def _create_friend_element(self, friend: Friend) -> ET.Element:
        """Create XML element for a friend declaration."""
        friend_elem = ET.Element("friend")
        friend_elem.set("type", friend.friend_type)
        friend_elem.set("name", friend.name)

        if friend.location:
            friend_elem.set("location", friend.location)

        return friend_elem

    def _prettify_xml(self, elem: ET.Element) -> str:
        """Return a pretty-printed XML string."""
        rough_string = ET.tostring(elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def generate_xml(self, parsed_header: ParsedHeader) -> str:
        """
        Generate XML for a parsed header.

        Args:
            parsed_header: ParsedHeader object

        Returns:
            Pretty-printed XML string
        """
        # Create root element
        root = ET.Element("header")
        root.set("file", parsed_header.relative_path)
        root.set("path", parsed_header.file_path)
        if parsed_header.base_path:
            root.set("base_path", parsed_header.base_path)

        # Add functions
        if parsed_header.functions:
            functions_elem = ET.SubElement(root, "functions")
            for func in parsed_header.functions:
                functions_elem.append(self._create_function_element(func))

        # Add structs
        if parsed_header.structs:
            structs_elem = ET.SubElement(root, "structs")
            for struct in parsed_header.structs:
                structs_elem.append(self._create_struct_element(struct))

        # Add classes
        if parsed_header.classes:
            classes_elem = ET.SubElement(root, "classes")
            for cls in parsed_header.classes:
                classes_elem.append(self._create_class_element(cls))

        # Add templates
        if parsed_header.templates:
            templates_elem = ET.SubElement(root, "templates")
            for template in parsed_header.templates:
                templates_elem.append(self._create_template_element(template))

        # Add enums
        if parsed_header.enums:
            enums_elem = ET.SubElement(root, "enums")
            for enum in parsed_header.enums:
                enums_elem.append(self._create_enum_element(enum))

        # Add unions
        if parsed_header.unions:
            unions_elem = ET.SubElement(root, "unions")
            for union in parsed_header.unions:
                unions_elem.append(self._create_union_element(union))

        # Add operators
        if parsed_header.operators:
            operators_elem = ET.SubElement(root, "operators")
            for operator in parsed_header.operators:
                operators_elem.append(self._create_operator_element(operator))

        return self._prettify_xml(root)

    def write_xml(self, pkg: str, parsed_header: ParsedHeader):
        """
        Write XML file for a parsed header.

        The output file structure mirrors the relative path of the source header.

        Args:
            parsed_header: ParsedHeader object
        """
        # Create output path mirroring the source structure
        relative_path = Path(parsed_header.relative_path)
        output_path = self.output_dir / pkg / relative_path.with_suffix('.xml')

        # Create output directory
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate and write XML
        xml_content = self.generate_xml(parsed_header)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)

        print(f"Generated: {output_path}")

    def generate_all(self, parsed_header_mapping: dict[str, list[ParsedHeader]]):
        """
        Generate XML files for all parsed headers.

        Args:
            parsed_headers: List of ParsedHeader objects
        """
        for pkg, parsed_headers in parsed_header_mapping.items():
            for parsed_header in parsed_headers:
                try:
                    self.write_xml(pkg, parsed_header)
                except Exception as e:
                    print(f"Error generating XML for {parsed_header.file_path}: {e}")
